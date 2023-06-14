import numpy as np
import cv2


# berechnet den Farbhistogramm mit angegebener Bin-anzahl (momentan 64,64,64) für das eingegebene Image
def calculate_histogram(image):
    hist = cv2.calcHist([image], [0, 1, 2], None, [64, 64, 64], [0, 256, 0, 256, 0, 256])
    cv2.normalize(hist, hist)
    return hist


# Berechne die Bhattacharyya-Distanz zwischen zwei Histogrammen
def bhattacharyya_distance(hist1, hist2):
    bcoeff = cv2.compareHist(hist1, hist2, cv2.HISTCMP_BHATTACHARYYA)
    bdist = np.sqrt(1 - bcoeff)
    return bdist


