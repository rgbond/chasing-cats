/*
 # Brightens a picture
 * Usage:  bright src dest alpha beta
 */

#include <cv.h>
#include <highgui.h>
#include <iostream>

using namespace cv;

int main( int argc, char** argv )
{
    Mat src = imread(argv[1]);

    double alpha = atof(argv[3]);
    int beta = atoi(argv[4]);


    Mat dest;
    src.convertTo(dest, -1, alpha, beta);

    imwrite(argv[2], dest);

    return 0;
}
