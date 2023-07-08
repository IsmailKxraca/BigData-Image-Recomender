import tensorflow as tf
import tensorflow.keras.applications.mobilenet_v3
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input
import numpy as np


# MobileNetV3-Modell laden, typ Large ausgewählt
model = tf.keras.applications.MobileNetV3Large(weights='imagenet', include_top=False, pooling='avg')


# Funktion zum Extrahieren des Feature-Vektors für ein Bild mit MobileNetV3
def extract_mobilenet_features(image_path):
    # Bild einlesen und vorverarbeiten
    img = image.load_img(image_path, target_size=(224, 224))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)

    # Feature-Vektor extrahieren
    features = model.predict(img)

    return features


def calculate_euclidean_distance(vector1, vector2):
    # Umwandlung der Vektoren in Numpy-Arrays
    vector1 = np.array(vector1)
    vector2 = np.array(vector2)

    # Berechnung des euklidischen Abstands
    distance = np.linalg.norm(vector1 - vector2)

    return distance

def cosine_similarity(vector1, vector2):
    vector1 = np.squeeze(vector1)
    vector2 = np.squeeze(vector2)
    dot_product = np.dot(vector1, vector2)
    norm1 = np.linalg.norm(vector1)
    norm2 = np.linalg.norm(vector2)
    similarity = dot_product / (norm1 * norm2)
    return similarity