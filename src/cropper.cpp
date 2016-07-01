/* 
 * Crops a picture 
 # cropper image from 256 x 256 to 227 x 227
 */
#include <opencv/cv.h>
#include <opencv/highgui.h>

using namespace cv;

int main( int argc, char** argv )
{
    char* imageName = argv[1];

    Mat image;
    image = imread( imageName, CV_LOAD_IMAGE_COLOR);

    if( argc != 2 || !image.data ) {
        printf( " No image data \n " );
        return -1;
    }

    if (image.cols <= 227 && image.rows <= 227)
        return 0;

    Rect r(14, 14, 227, 227);
    Rect fr(0, 0, image.cols, image.rows);
    r = r & fr;

    Mat cropped = image(r);

    imwrite(imageName, cropped);

    /* 
    namedWindow( "original", CV_WINDOW_AUTOSIZE );
    namedWindow( "cropped", CV_WINDOW_AUTOSIZE );

    imshow("original", image);
    imshow("cropped", cropped);

    waitKey(0);
    */

    return 0;
}
