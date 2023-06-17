import numpy as np
import cv2


# berechnet den Farbhistogramm mit angegebener Bin-anzahl (momentan 8,8,8) für das eingegebene Image
def calculate_histogram(image):
    hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
    #cv2.normalize(hist, hist)
    return hist


# Berechne die Bhattacharyya-Distanz zwischen zwei Histogrammen
def bhattacharyya_distance(hist1, hist2):
    bcoeff = cv2.compareHist(hist1, hist2, cv2.HISTCMP_BHATTACHARYYA)
    bdist = np.sqrt(1 - bcoeff)
    return bdist


hist = calculate_histogram(cv2.imread(r"C:\Users\Ismai\OneDrive\Desktop\train2017\000000001393.jpg"))
print(str(hist))