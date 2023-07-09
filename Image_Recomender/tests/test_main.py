import cv2
import numpy as np
import pandas as pd
from skimage import metrics
from Image_Recomender.code.embeddings import extract_mobilenet_features
from Image_Recomender.code.embeddings import cosine_similarity
from Image_Recomender.code.colour import calculate_histogram
from Image_Recomender.code.colour import bhattacharyya_distance

input_image = "test_input_image.jpg"
test_daten = "test_images"

# the expected dcitionaries of the functions
expected_dict_hist = {1: 0.5365889817405047, 2: 0.38757068990477367, 3: 0.4458220732372323, 4: 0.5845114832923415, 5: 0.5673833568216253, 6: 0.6612573463639158, 7: 0.403657289478365, 8: 0.5885265128678128, 9: 0.6189604956971404, 10: 0.515588198905021, 11: 0.6044244658451768, 12: 0.5046903954347617, 13: 0.5163159157752194, 14: 0.5837276467814251, 15: 0.6265899978229115, 16: 0.4884938186850638, 17: 0.33004443827785773, 18: 0.48557902744380105, 19: 0.5291690643687436, 20: 0.6208446250087607, 21: 0.4308275510277483, 22: 0.5354785467608748, 23: 0.4013973464914965, 24: 0.5415889624813591, 25: 0.5484581355129535, 26: 0.5921847873252379, 27: 0.27214384887421916}
expected_dict_ssim = {1: 0.23341575086102587, 2: 0.42097546810260206, 3: 0.3219279831678777, 4: 0.20825187872484635, 5: 0.047026671375041226, 6: 0.10607505848049045, 7: 0.3546526187251994, 8: 0.2084008927407136, 9: 0.1425934450978756, 10: 0.19774291347906117, 11: 0.1260412784860367, 12: 0.21089201872709015, 13: 0.16943590590369897, 14: 0.10821758523083469, 15: 0.10141868887731767, 16: 0.35723758317128623, 17: 0.22248575659921924, 18: 0.2505748799909201, 19: 0.208335747291038, 20: 0.11736850686664985, 21: 0.29296489200102804, 22: 0.2718849851100256, 23: 0.1123102423777476, 24: 0.30331846029300885, 25: 0.15532578807225708, 26: 0.3125703069659343, 27: 0.21201327757359298}
expected_dict_embeddings = {1: 0.2103859, 2: 0.17940193, 3: 0.28625512, 4: 0.21160276, 5: 0.2649729, 6: 0.21226262, 7: 0.20630822, 8: 0.22372298, 9: 0.18436818, 10: 0.30539498, 11: 0.2899256, 12: 0.21232763, 13: 0.20925167, 14: 0.2638035, 15: 0.225748, 16: 0.16992505, 17: 0.24508408, 18: 0.14907216, 19: 0.2546608, 20: 0.22841892, 21: 0.17135346, 22: 0.26652443, 23: 0.12213264, 24: 0.2249781, 25: 0.23968215, 26: 0.31964833, 27: 0.20194015}


# tests whether the funtion return the right Dictionary
def test_hist_vergleich(input_img):
    new_img = cv2.imread(input_img)
    new_hist = calculate_histogram(new_img)

    compare_dict = {}
    df = pd.read_pickle("histograms.pkl")
    for index, row in df.iterrows():
        cur_id = row["Id"]
        cur_hist = row["Histogram"]
        compare_dict[cur_id] = bhattacharyya_distance(new_hist, cur_hist)

    assert comapre_dict == expected_dict_hist


# tests whether the funtion return the right Dictionary
def test_ssim_vergleich(input_img):
    new_img = cv2.imread(input_img)

    resized_image = cv2.resize(new_img, (128, 128))
    gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
    new_ssim = np.reshape(gray_image, (128 * 128))

    compare_dict = {}
    df = pd.read_pickle("ssim.pkl")
    for index, row in df.iterrows():
        cur_id = row["Id"]
        cur_ssim = row["Ssim"]
        compare_dict[cur_id] = metrics.structural_similarity(new_ssim, cur_ssim)

    assert comapre_dict == expected_dict_ssim


# tests whether the funtion return the right Dictionary
def test_embeddings_vergleich(input_img):
    new_features = extract_mobilenet_features(input_img)
    print(new_features)
    compare_dict = {}
    df = pd.read_pickle("embeddings.pkl")
    for index, row in df.iterrows():
        cur_id = row["Id"]
        cur_features = row["Feature_vector"]
        compare_dict[cur_id] = cosine_similarity(new_features, cur_features)

    assert compare_dict == expected_dict_embeddings



