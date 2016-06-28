/*
 * Simple examle to use to debug opencv installatins
 */

#include <iostream>
#include "opencv2/opencv.hpp"
#include "opencv2/gpu/gpu.hpp"

using namespace std;
using namespace cv;
using namespace cv::gpu;

int main (int argc, char* argv[])
{
    try
    {
        Mat src_host = cv::imread("../images/ecat/MDAlarm_20160531-231431.jpg", CV_LOAD_IMAGE_GRAYSCALE);
        GpuMat dst, src;
        src.upload(src_host);
        gpu::threshold(src, dst, 128.0, 255.0, CV_THRESH_BINARY);
        Mat result_host;
        dst.download(result_host);
        imshow("Result", result_host);
        waitKey();
    }
    catch(const cv::Exception& ex)
    {
        cout << "Error: " << ex.what() << std::endl;
    }
    return 0;
}
