/*
 * Foreground extraction routine
 * Usage:
 * extract_fg photo bg_photo dest_dir seg_dir
 *      Subtracts bg_photo from photo. Saves photo in dest_dir and segmenation in seg_dir
 *
 * extract_fg -s photo dest_dir seg_dir
 *      Edits photo and segmentation in seg_dir, saves in dest_dir and seg_dir
 *
 * Use the mouse to select an area then hit a key on the keyboard:
 *      c - clear all pixels in the selection
 *      s - set all pixels in the selection
 *      w - magnifies the selection in another window
 *      1,2,3,4,6,8: sets the magnification for the next "w" command
 *      a,o,e - work on cat, dog or person pixels, defaults to cat
 *      d - attempnt to find and clear shadown pixels
 *      q - save files and exit
 *      ESC - exit without saving files
 *
 */

#include <sys/types.h>
#include <iostream>
#include <stdio.h>
#include <unistd.h>
#include <math.h>

#include "opencv2/core/core.hpp"
#include "opencv2/gpu/gpu.hpp"
#include "opencv2/highgui/highgui.hpp"

using namespace std;
using namespace cv;
using namespace cv::gpu;

const uint8_t cat_seg_value = 17;
const uint8_t dog_seg_value = 18;
const uint8_t person_seg_value = 19;

// #define USE_VIBE

// options
bool use_bg_photo = true;
string photo_filename;
string bg_filename;
string dest_jpg;    // A copy of photo_filename
string dest_png;    // The segmented image
string dest_dir;
string seg_dir;

void parse_options(int argc, char *argv[])
{
    int c;

    while ((c = getopt(argc, argv, "sv")) != -1) {
        switch (c) {
            case 's':
                use_bg_photo = false;
                printf("Don't use bg photo\n");
                break;
            default:
                printf("Huh\n");
                exit(1);
        }
    }
    int nargs = use_bg_photo ? 4 : 3;
    if (optind + nargs != argc) {
        printf("usage: extract_fg photo bg dest_dir seg_dir\n");
        printf("       extract_fg -s photo dest_dir seg_dir\n");
        exit(1);
    }

    photo_filename = string(argv[optind++]);
    if (use_bg_photo)
        bg_filename = string(argv[optind++]);
    dest_dir = string(argv[optind++]);
    seg_dir = string(argv[optind++]);

    size_t i = photo_filename.rfind("/", photo_filename.length());
    string pfn = photo_filename.substr(i+1, photo_filename.length() - 1);
    i = pfn.find(".");
    string pb = pfn.substr(0, i);
    dest_jpg = dest_dir + string("/") + pfn;
    dest_png = seg_dir + string("/") + pb + string(".png");
}

// globals
GpuMat d_bg;
Mat bg;
Mat frame;
Mat fg_src;
Mat fg;
int mag = 4;
int cur_seg_value = cat_seg_value;

static void grab_background()
{
    bg = imread(bg_filename.c_str());
    if (bg.empty()) {
        printf("Can't read background frame %s!\n",
               bg_filename.c_str());
        exit(1);
    }
    imshow("bg", bg);

    try {
        GpuMat d_tmp(bg);
        gpu::GaussianBlur(d_tmp, d_bg, Size(3, 3), 0.0, 0,0);
    }
    catch (int e) {
        cout << "Exception: " << e << " on GPU acess in grab_background" << endl;
    }
}

void reload_fg(uint8_t cur_seg)
{
    fg = Mat::zeros(fg_src.rows, fg_src.cols, CV_8UC1);

    for (int y = 0; y < fg_src.rows; y++) {
        for (int x = 0; x < fg_src.cols; x++) {
            uint8_t c = fg_src.at<uchar>(y, x);
            if (c == cur_seg)
                fg.at<uchar>(y, x) = 255;
            else if (c > 0)
                fg.at<uchar>(y, x) = 128;
        }
    }
}

static void save_files()
{
    Mat oframe = Mat::zeros(frame.rows, frame.cols, CV_8UC1);

    for (int y = 0; y < fg.rows; y++) {
        for (int x = 0; x < fg.cols; x++) {
            uint8_t c = fg.at<uchar>(y, x);
            if (c > 0)
                oframe.at<uchar>(y, x) = fg_src.at<uchar>(y, x);
        }
    }

    cout << "Writing: " << dest_jpg << " " << dest_png << endl;

    string system_cmd = "cp " + photo_filename + " " + dest_jpg;
    system(system_cmd.c_str());
    imwrite(dest_png.c_str(), oframe);
}

void clear_shadows()
{
    for (int y = 0; y < frame.rows; y++) {
        for (int x = 0; x < frame.cols; x++) {
            uchar f = fg.at<uchar>(y, x);
            if (f > 250) {
                Vec3b fp = frame.at<Vec3b>(y, x);
                Vec3b bp = bg.at<Vec3b>(y, x);
                int ncolor = 0;
                for (int i = 0; i < 3; i++) {
                    int delta = bp[i] - fp[i];
                    if (delta > 0 && delta < 40)
                        ncolor++;
                }
                if (ncolor == 3)
                    fg.at<uchar>(y, x) = 0;
            }
        }
    }
}

uchar mag_tbl[256];

// Adaptive linear table...
// Adjusts contrast of items in the roi window
void build_mag_tbl(Mat &photo_sub, Mat &fg_sub)
{
    const float b0 = 50.0;
    const float b1 = 250.0;
    int min = 255.0;
    int max = 0.0;
    for (int y = 0; y < photo_sub.rows; y++) {
        for (int x = 0; x < photo_sub.cols; x++) {
            uchar f = fg_sub.at<uchar>(y, x);
            if (f > 250) {
                Vec3b p = photo_sub.at<Vec3b>(y, x);
                for (int i = 0; i < 3; i++) {
                    if  (p[i] < min)
                        min = p[i]; 
                    if (p[i] > max)
                        max = p[i]; 
                }
            }
        }
    }
    float a = (b1-b0)/(float)(max - min);
    float b = b1 - a * (float)max;
    // cout << "a, b " <<  " " << a << " " << b << endl;

    for (int i = 0; i < 256; i++)
        mag_tbl[i] = saturate_cast<uchar>((int)(a * (float) i + b + 0.5));
}

// Nice blocky pixels, no anti-aliasing
void blk_resize(Mat &photo_sub, Mat &fg_sub, Mat &dest)
{
    build_mag_tbl(photo_sub, fg_sub);
    int xf = dest.cols / fg_sub.cols;
    int yf = dest.rows / fg_sub.rows;
    assert(xf >= 1 && yf >= 1);
    assert(fg_sub.type() == CV_8UC1 && dest.type() == CV_8UC3);
    for (int y = 0; y < dest.rows; y++) {
        for (int x = 0; x < dest.cols; x++) {
            uchar f = fg_sub.at<uchar>(y / yf, x / xf);
            if (f > 250) {
                Vec3b p = photo_sub.at<Vec3b>(y / yf, x / xf);
                p[0] = mag_tbl[p[0]];
                p[1] = mag_tbl[p[1]];
                p[2] = mag_tbl[p[2]];
                dest.at<Vec3b>(y, x) = p;
            } else {
                dest.at<Vec3b>(y, x) = Vec3b(0, 0, 0);
            }
        }
    }
}


// TODO This really needs to be a window class... Would clean up on_mouse() and
// clean up the subroutines supporting the case statement in main()
struct mouse_info {
    string window;
    bool select_flag;
    bool drag;
    Point point1;
    Rect roi;
    Mat *pmat;
};

static void on_mouse(int event, int x, int y, int flags, void *userdata)
{
    struct mouse_info *mi = (struct mouse_info *) userdata;
    if (event == CV_EVENT_LBUTTONDOWN && !mi->drag) {
        mi->select_flag = false;
        mi->point1 = Point(x, y);
        mi->drag = true;
    }
    if (event == CV_EVENT_MOUSEMOVE && mi->drag) {
        Mat m = mi->pmat->clone();
        Point point2 = Point(x, y);
        Rect rect = Rect(mi->point1, point2);
        Rect ir(0, 0, mi->pmat->cols, mi->pmat->rows);
        rect = rect & ir;
        bitwise_not(m(rect), m(rect));
        imshow(mi->window.c_str(), m);
    }
    if (event == CV_EVENT_LBUTTONUP && mi->drag) {
        mi->drag = false;
        Point point2 = Point(x, y);
        mi->roi = Rect(mi->point1, point2);
        Rect ir(0, 0, mi->pmat->cols, mi->pmat->rows);
        mi->roi = mi->roi & ir;
        mi->select_flag = true;
    }
}

struct adj {
    double alpha;
    double beta;
} adj[] = {
    { 1.0, 4.0 },
    { 1.0, 2.0 },
    { 1.0, 1.0 },
    { 1.0, 1.0 },
    { 1.0, 0.0 },
    { 1.0, 0.0 },
    { 1.0, 0.0 },
    { 1.0, -1.0 },
    { 1.0, -1.0 },
    { 1.0, -2.0 },
    { 1.0, -4.0 },
};

// Main pixel processing
void process_frame()
{
#ifdef USE_VIBE
    gpu::VIBE_GPU *pbg = new VIBE_GPU();
#else
    gpu::MOG2_GPU *pbg = new MOG2_GPU();
    pbg->nShadowDetection = 255;
#endif
    GpuMat d_fg;

    for (int i = 0; i < sizeof(adj)/sizeof(struct adj); i++) {
        GpuMat d_adj;
        d_bg.convertTo(d_adj, -1, adj[i].alpha, adj[i].beta); 
        pbg->operator()(d_adj, d_fg);
    }
    GpuMat d_frame(frame);

    GpuMat d_tmp;
    gpu::GaussianBlur(d_frame, d_tmp, Size(3, 3), 0.0, 0,0);

    pbg->operator()(d_tmp, d_fg);
    d_fg.download(fg);

    // Clear out the frame header in fg
    Rect to_clear(0, 0, 240, 30);
    fg(to_clear).setTo(Scalar(0));

    // Load fg_src, assuming they are all cat pixels
    fg_src = Mat::zeros(fg.rows, fg.cols, CV_8UC1);

    for (int y = 0; y < fg.rows; y++) {
        for (int x = 0; x < fg.cols; x++) {
            uint8_t c = fg.at<uchar>(y, x);
            if (c >= 250)
                fg_src.at<uchar>(y, x) = cat_seg_value;
        }
    }
}

// Set the segment we are working on
void set_seg_value(int v)
{
    cur_seg_value = v;
    reload_fg(cur_seg_value);
    imshow("fg", fg);
}

// Map an roi window selection to the main window
Rect get_fg_rect(mouse_info &fg_window, mouse_info &roi_window)
{
    Point fg_point1(fg_window.roi.x + roi_window.roi.x / mag,
                    fg_window.roi.y + roi_window.roi.y / mag);
    Size fg_size(roi_window.roi.width / mag, roi_window.roi.height / mag);
    return Rect(fg_point1, fg_size);
}
   
// Propogate info from main window & refresh roi window
void refresh_roi(mouse_info &fg_window, mouse_info &roi_window)
{
    Mat fg_sub = fg(fg_window.roi);
    Mat photo_sub = frame(fg_window.roi);
    *roi_window.pmat = Mat(fg_window.roi.height * mag, fg_window.roi.width * mag, CV_8UC3);
    blk_resize(photo_sub, fg_sub, *roi_window.pmat);
    imshow("roi", *roi_window.pmat);
    roi_window.select_flag = false;
    roi_window.drag = false;
}

// Set or clear pixels in the selected roi
void set_roi(mouse_info &fg_window, mouse_info &roi_window, Scalar v1, Scalar v2)
{
    if (fg_window.select_flag) {
        fg(fg_window.roi).setTo(v1);
        fg_src(fg_window.roi).setTo(v2);
        imshow("fg", fg);
        fg_window.select_flag = false;
    } else if (roi_window.select_flag) {
        Rect fg_rect = get_fg_rect(fg_window, roi_window);
        fg(fg_rect).setTo(v1);
        fg_src(fg_rect).setTo(v2);
        imshow("fg", fg);
        refresh_roi(fg_window, roi_window);
    }
}

int main(int argc, char* argv[])
{
    int64 st;
    FILE *fp;

    printf("extract_fg\n");
    parse_options(argc, argv);
    fflush(stdout);

    namedWindow("photo", CV_WINDOW_AUTOSIZE);
    if (use_bg_photo)
        namedWindow("bg", CV_WINDOW_AUTOSIZE);
    namedWindow("fg", CV_WINDOW_AUTOSIZE);
    namedWindow("roi", CV_WINDOW_AUTOSIZE);

    moveWindow("photo", 100, 100);
    if (use_bg_photo)
        moveWindow("bg", 800, 100);
    moveWindow("fg", 100, 550);
    moveWindow("roi", 800, 550);

    struct mouse_info fg_window;
    fg_window.window = string("fg");
    fg_window.select_flag = false;
    fg_window.drag = false;
    fg_window.pmat = &fg;
    setMouseCallback("fg", on_mouse, &fg_window);

    Mat big_fg;
    struct mouse_info roi_window;
    roi_window.window = string("roi");
    roi_window.pmat = &big_fg;

    frame = imread(photo_filename.c_str());

    if (use_bg_photo) {
        grab_background();
        process_frame();
    } else {
        fg_src = imread(dest_png.c_str(), CV_LOAD_IMAGE_GRAYSCALE);
        assert(!fg_src.empty());
        assert(fg_src.rows == frame.rows && fg_src.cols == frame.cols);
        assert(fg_src.type() == CV_8UC1);
        reload_fg(cur_seg_value);
    }

    imshow("fg", fg);
    imshow("photo", frame);

    bool done = false;
    while(!done)
    {
        int key = waitKey(0);
        if (key == -1)
            continue;
        key &=  0xff;
        switch (key) {
            case 27:
                done = true;
                break;
            case 'q':
                done = true;
                save_files();
                imshow("fg", fg);
                break;
            case 'a':
                set_seg_value(cat_seg_value);
                break;
            case 'o':
                set_seg_value(dog_seg_value);
                break;
            case 'e':
                set_seg_value(person_seg_value);
                break;
            case '1':
            case '2':
            case '3':
            case '4':
            case '6':
            case '8':
                mag = key - '0';
                break;
            case 'd':
                clear_shadows();
                imshow("fg", fg);
                break;
            case 'c':
                set_roi(fg_window, roi_window, Scalar(0), Scalar(0));
                break;
            case 's':
                set_roi(fg_window, roi_window, Scalar(255), Scalar(cur_seg_value));
                break;
            case 'w':
                if (fg_window.select_flag) {
                    imshow("fg", fg);
                    fg_window.select_flag = false;
                    refresh_roi(fg_window, roi_window);
                    setMouseCallback("roi", on_mouse, &roi_window);
                }
            default:
                break;
        }
    }



    destroyWindow("fg");
    destroyWindow("photo");
    if (use_bg_photo)
        destroyWindow("bg");
    destroyWindow("roi");

    if (use_bg_photo)
        d_bg.release();

    exit(0);
}
