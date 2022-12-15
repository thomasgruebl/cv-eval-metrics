#include <iostream>
#include <stdexcept>
#include <cmath>
#include <opencv2/opencv.hpp>


extern "C" long double mcc(const char *test_image_path, const char *ground_truth_path) {
	long double TP =0, TN = 0, FP = 0, FN = 0;
	
	cv::Mat ground_truth;
	cv::Mat test_image;
	
	ground_truth = cv::imread(ground_truth_path, cv::IMREAD_GRAYSCALE);
	test_image = cv::imread(test_image_path, cv::IMREAD_GRAYSCALE);
	
	double ret1, ret2;
	ret1 = cv::threshold(test_image, test_image, 127, 255, cv::THRESH_BINARY);
    ret2 = cv::threshold(ground_truth, ground_truth, 127, 255, cv::THRESH_BINARY);
	
	if ((ground_truth.size().width != test_image.size().width) || 
		(ground_truth.size().height != test_image.size().height))
	{
		throw std::length_error("Image dimesions must match.");
	}
	
	cv::Mat mask1, mask2;
	cv::inRange(test_image, cv::Scalar(0), cv::Scalar(0), mask1);
	cv::inRange(ground_truth, cv::Scalar(0), cv::Scalar(0), mask2);
    test_image.setTo(cv::Scalar(1), mask1);
	ground_truth.setTo(cv::Scalar(2), mask2);
	test_image.convertTo(test_image, CV_32FC1);
	ground_truth.convertTo(ground_truth, CV_32FC1);
	
	cv::Mat res;
	res.convertTo(res, CV_32FC1);
	cv::multiply(test_image, ground_truth, res);
	
	TP = cv::countNonZero(res == 65025);
    FP = cv::countNonZero(res == 255);
    TN = cv::countNonZero(res == 2);
    FN = cv::countNonZero(res == 510);
	
	// std::cout << TP << std::endl << TN << std::endl << FN << std::endl << FP << std::endl;
	
	// identical images
	if (FP == 0 && FN == 0)
	{
		return 1.0;
	}
	// no pixels matching
	else if (TP == 0 && TN == 0)
	{
		return -1.0;
	}
	
	return ((long double)((TP * TN) - (FP * FN))) / (sqrt((long double)((TP + FP) * (TP + FN) * (TN + FP) * (TN + FN))));
}
