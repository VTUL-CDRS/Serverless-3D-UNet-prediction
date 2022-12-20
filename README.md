# Online-prediction
Online prediction using 3D U-Net tensorflow model

## Architecture

![Architecture](images/architecture.png)

## Components
* [AWS Amplify](): A website for user to upload files and download the prediction result.
* [AWS Lambda](): A serverless function to handle the prediction request and save the prediction output as an image to AWS S3.
* [AWS Sagemaker](): Hosting machine learning model to predict the segmentation mask of the uploaded image.

