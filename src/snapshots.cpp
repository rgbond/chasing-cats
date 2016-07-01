/*
 * Convert a movie to a set of still frames
 */
#include <iostream>
#include <stdio.h>

#include "opencv2/core/core.hpp"
#include "opencv2/gpu/gpu.hpp"
#include "opencv2/highgui/highgui.hpp"

using namespace std;
using namespace cv;
using namespace cv::gpu;

int main(int argc, char* argv[])
{
	int64 st;
	Mat frame;

    // open the video file for reading
    VideoCapture cap(0);

    if (!cap.isOpened()) {
         cout << "Cannot open the video file" << endl;
         return -1;
    }

	if (!cap.read(frame)) {
         cout << "Cannot read the video file" << endl;
         return -1;
    }

    namedWindow("vid", CV_WINDOW_AUTOSIZE);

    int frame_number = 0;
    bool done = false;
    while(!done) {
		double dt;
        cap.read(frame); // read a new frame from video

		if (frame.empty())
			break;

        imshow("vid", frame);

        // Wait 1ms or for any key
        int key;
        key = waitKey(1) & 0xff;
        switch(key) {
        case 27:
        case 'q':
            done = true;
            break;
        case 's':
            frame_number++;
            char file_name[50];
            sprintf(file_name, "snap_%02d.png", frame_number);
            imwrite(file_name, frame);
            break;
        }
    }

    return 0;
}
