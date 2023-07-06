import cv2
import numpy as np
import pandas as pd
import pickle
from skimage import transform
from skimage.metrics import structural_similarity as ssim

def calculate_similarity(target_image_path, pickle_file_path):
    
    # Zielbild öffnen und auf 128x128 Pixel skalieeren
    target_image = cv2.imread(target_image_path, cv2.IMREAD_GRAYSCALE)
    target_image = transform.resize(target_image, (128, 128), mode='reflect')

    # Variable für einmal das ähnlichste Bild und den Ähnlichkeitswert der halt der beste sein muss
    best_image = None
    best_ssim = 1

    # Bilddaten laden aus der pickle datei
    with open(pickle_file_path, 'rb') as f:
        image_data = pickle.load(f)

    # Bilder werden durchlaufen
    for image_info in image_data:
        bild = cv2.imread(image_info['ImagePath'], cv2.IMREAD_GRAYSCALE)
        bild = transform.resize(bild, (128, 128), mode='reflect')

        # SSIM berechnen
        ssim_score = ssim(target_image, bild)

        # Checken ob der aktuelle Ähnlichkeitswert besser ist als der bisher beste
        if ssim_score > best_ssim:
            best_ssim = ssim_score
            best_image = bild

    return best_image , best_ssim # Bestes bild UND SSIM wert wird ausgegeben