import boto3
import numpy as np
import os
import segmentation_models_3D as sm
import sys
import tensorflow as tf

from keras.models import load_model
from patchify import patchify, unpatchify
from skimage import io
from tifffile import imwrite
from sagemaker.tensorflow import TensorFlowPredictor

s3 = boto3.client('s3')


def convert(img, target_type_min, target_type_max, target_type):
    imin = img.min()
    imax = img.max()

    a = (target_type_max - target_type_min) / (imax - imin)
    b = target_type_max - a * imax
    new_img = (a * img + b).astype(target_type)
    return new_img


def handler(event, context):

    s3_event = event['Records'][0]['s3']
    bucket_name = s3_event['bucket']['name']
    object_key = s3_event['object']['key']
    predict_file = object_key.replace('.tif', '_predict.tif')
    sagemaker_endpoint = os.getenv('SAGEMAKER_ENDPOINT')

    if ('result/' not in object_key):

        print("Download file")
        s3.download_file(bucket_name, object_key, '/tmp/' + object_key)

        print("Prediction......")
        predictor = TensorFlowPredictor(sagemaker_endpoint)
        inputimage = io.imread('/tmp/' + object_key)

        patches = patchify(inputimage, (64, 64, 64), step=64)
        BACKBONE = 'vgg16'
        preprocess_input = sm.get_preprocessing(BACKBONE)

        predicted_patches = []
        for i in range(patches.shape[0]):
            for j in range(patches.shape[1]):
                for k in range(patches.shape[2]):
                    single_patch = patches[i, j, k, :, :, :]
                    single_patch_3ch = np.stack((single_patch,)*3, axis=-1)
                    single_patch_3ch_input = preprocess_input(
                        np.expand_dims(single_patch_3ch, axis=0))
                    single_patch_prediction = predictor.predict(
                        single_patch_3ch_input)
                    predictlist = single_patch_prediction['predictions'][0]
                    single_patch_prediction_result = np.squeeze(
                        predictlist)
                    predicted_patches.append(single_patch_prediction_result)

        predicted_patches = np.array(predicted_patches)

        predicted_patches_reshaped = np.reshape(predicted_patches,
                                                (patches.shape[0], patches.shape[1], patches.shape[2],
                                                 patches.shape[3], patches.shape[4], patches.shape[5]))

        reconstructed_image = unpatchify(
            predicted_patches_reshaped, inputimage.shape)

        imgu8 = convert(reconstructed_image, 0, 255, np.uint8)
        imwrite('/tmp/' + predict_file, imgu8)

        print("Upload the file")
        s3.upload_file('/tmp/' + predict_file, bucket_name,
                       'result/' + predict_file)

    return {
        "statusCode": 200
    }
