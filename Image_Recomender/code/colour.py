import numpy as np
import cv2


# calculates the color-histogramm of the input image with (8,8,8) Bins
def calculate_histogram(image):
    hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
    cv2.normalize(hist, hist)
    return hist


# calculates the bhattacharyya-distance between to histograms and turns it into similarity
def bhattacharyya_distance(hist1, hist2):
    bcoeff = cv2.compareHist(hist1, hist2, cv2.HISTCMP_BHATTACHARYYA)
    bdist = np.sqrt(1 - bcoeff)

    return bdist
