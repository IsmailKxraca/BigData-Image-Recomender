import tensorflow as tf
import tensorflow.keras.applications.mobilenet_v3
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input
import numpy as np


# load MobileNetV3-Modell, type Large, without last output-Layer
model = tf.keras.applications.MobileNetV3Large(weights='imagenet', include_top=False, pooling='avg')


# function for extracting the feature-vector of a image with MobileNetV3
def extract_mobilenet_features(image_path):
    # read image and process it so we can work with it
    img = image.load_img(image_path, target_size=(224, 224))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)

    # extract feature-vector
    features = model.predict(img)

    return features


# calculate the cosine-similarity of two vectors
def cosine_similarity(vector1, vector2):
    # process vectors
    vector1 = np.squeeze(vector1)
    vector2 = np.squeeze(vector2)
    dot_product = np.dot(vector1, vector2)
    norm1 = np.linalg.norm(vector1)
    norm2 = np.linalg.norm(vector2)
    similarity = dot_product / (norm1 * norm2)

    return similarity