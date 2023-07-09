import cv2
import numpy as np
import os
import sys
from Image_Recomender.code.colour import calculate_histogram
from Image_Recomender.code.colour import bhattacharyya_distance
import Image_Recomender.code.database as database
import pandas as pd
import pickle
import heapq
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from Image_Recomender.code.embeddings import extract_mobilenet_features
from Image_Recomender.code.embeddings import cosine_similarity
from skimage import metrics

conn = database.connect_test_database()


# load the histograms into a pickle file
def read_pickle_hist():
    df_restored = pd.read_pickle("histograms.pkl")
    print(df_restored.info())
    return df_restored


# load the resized and grayscaled images into a pickle file
def read_pickle_ssim():
    df_restored = pd.read_pickle("ssim.pkl")
    return df_restored


# load the feature vectors into a pickle file
def read_pickle_embeddings():
    df_restored = pd.read_pickle("embeddings.pkl")
    return df_restored


# input = dictionary with all similarities. Output = list with Ids of the top five highest values.
def topfive(dict):
    largest_values = heapq.nlargest(5, dict, key=dict.get)

    return largest_values


def topfive_embeddings(dict):
    smallest_values = heapq.nsmallest(5, dict, key=dict.get)

    return smallest_values


# generator for comparing the Input-Image with all of the histograms saved in the pickle file.
# Output = dictionary with all similarities
def hist_vergleich(input_img):
    new_img = cv2.imread(input_img)
    new_hist = calculate_histogram(new_img)

    compare_dict = {}
    df = read_pickle_hist()
    for index, row in df.iterrows():
        cur_id = row["Id"]
        cur_hist = row["Histogram"]
        compare_dict[cur_id] = bhattacharyya_distance(new_hist, cur_hist)

    return compare_dict


# function for comparing the Input-Image with all of the scaled images saved in the pickle file.
# Output = dictionary with all similarities
def ssim_vergleich(input_img):
    new_img = cv2.imread(input_img)

    resized_image = cv2.resize(new_img, (128, 128))
    gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
    new_ssim = np.reshape(gray_image, (128 * 128))

    compare_dict = {}
    df = read_pickle_ssim()
    for index, row in df.iterrows():
        cur_id = row["Id"]
        cur_ssim = row["Ssim"]
        compare_dict[cur_id] = metrics.structural_similarity(new_ssim, cur_ssim)

    return compare_dict


def embeddings_vergleich(input_img):
    new_features = extract_mobilenet_features(input_img)
    print(new_features)
    compare_dict = {}
    df = read_pickle_embeddings()
    for index, row in df.iterrows():
        cur_id = row["Id"]
        cur_features = row["Feature_vector"]
        compare_dict[cur_id] = cosine_similarity(new_features, cur_features)

    return compare_dict


# plots the top five most similar images for histograms
# conn = database, top_five_list = topfive function output, dict = compare dictionary
def zeige_bilder_hist(conn, top_five_list, dict):
    # gets the full image paths of the top five IDs
    path_liste = []
    for id in top_five_list:
        path_liste.append(database.get_path_from_id(conn, id))

    fig, axes = plt.subplots(nrows=1, ncols=5, figsize=(12, 4))

    # plots all five images with the similarity as text next to each other.
    for i in range(5):
        image_path = path_liste[i]
        image = mpimg.imread(image_path)
        axes[i].imshow(image)
        axes[i].axis('off')

        fig.text(0.5, 0.95, 'Farbschema', fontsize=12, color='white', backgroundcolor="black", weight="bold",
                  ha='center', va='center')
        text = f"{round(dict[top_five_list[i]]*100,3)}% Ähnlichkeit"
        axes[i].text(0, 0, text, color='white', backgroundcolor='black', fontsize=10, weight='bold')

    # final plot
    plt.tight_layout()
    plt.show()


# plots the top five most similar images for ssim
# conn = database, top_five_list = topfive function output, dict = compare dictionary
def zeige_bilder_ssim(conn, top_five_list, dict):
    # gets the full image paths of the top five IDs
    path_liste = []
    for id in top_five_list:
        path_liste.append(database.get_path_from_id(conn, id))

    fig, axes = plt.subplots(nrows=1, ncols=5, figsize=(12, 4))

    # plots all five images with the similarity as text next to each other.
    for i in range(5):
        image_path = path_liste[i]
        image = mpimg.imread(image_path)
        axes[i].imshow(image)
        axes[i].axis('off')

        fig.text(0.5, 0.95, 'Structural similarity index', fontsize=12, color='white', backgroundcolor="black", weight="bold",
                  ha='center', va='center')
        text = f"{round(dict[top_five_list[i]]*100,3)}% Ähnlichkeit"
        axes[i].text(0, 0, text, color='white', backgroundcolor='black', fontsize=10, weight='bold')

    # final plot
    plt.tight_layout()
    plt.show()


# plots the top five most similar images for embedding
# conn = database, top_five_list = topfive function output, dict = compare dictionary
def zeige_bilder_embedding(conn, top_five_list, dict):
    # gets the full image paths of the top five IDs
    path_liste = []
    for id in top_five_list:
        path_liste.append(database.get_path_from_id(conn, id))

    fig, axes = plt.subplots(nrows=1, ncols=5, figsize=(12, 4))

    # plots all five images with the similarity as text next to each other.
    for i in range(5):
        image_path = path_liste[i]
        image = mpimg.imread(image_path)
        axes[i].imshow(image)
        axes[i].axis('off')

        fig.text(0.5, 0.95, 'Embedding (MobileNet Features)', fontsize=12, color='white', backgroundcolor="black", weight="bold",
                  ha='center', va='center')
        text = f"{round(dict[top_five_list[i]]*100,3)}% Ähnlichkeit"
        axes[i].text(0, 0, text, color='white', backgroundcolor='black', fontsize=10, weight='bold')

    # final plot
    plt.tight_layout()
    plt.show()


# main function for color-scheme, where you can give an input image and get the plots of the most similar images.
def main_hist(input_image):
    dict = hist_vergleich(input_image)

    top_five = topfive(dict)
    image = mpimg.imread(input_image)

    # create figure
    fig2 = plt.figure()

    plt.imshow(image)
    fig2.text(0.5, 0.95, 'Input Image', fontsize=12, color='red', backgroundcolor="black",weight="bold", ha='center', va='center')
    plt.axis('off')

    plt.show(block=False)

    zeige_bilder_hist(conn, top_five, dict)


# main function for ssim
def main_ssim(input_image):
    dict = ssim_vergleich(input_image)

    top_five = topfive(dict)

    image = mpimg.imread(input_image)

    # create figure
    fig2 = plt.figure()

    plt.imshow(image)
    fig2.text(0.5, 0.95, 'Input Image', fontsize=12, color='red', backgroundcolor="black",weight="bold", ha='center', va='center')
    plt.axis('off')

    plt.show(block=False)

    zeige_bilder_ssim(conn, top_five, dict)


# main function for embedding
def main_embedding(input_image):
    dict = embeddings_vergleich(input_image)

    top_five = topfive(dict)

    image = mpimg.imread(input_image)

    # create figure
    fig2 = plt.figure()

    plt.imshow(image)
    fig2.text(0.5, 0.95, 'Input Image', fontsize=12, color='red', backgroundcolor="black",weight="bold", ha='center', va='center')
    plt.axis('off')

    plt.show(block=False)

    zeige_bilder_embedding(conn, top_five, dict)

if __name__ == "__main__":
    # database.show_path(conn)
    # main_hist(r"D:\images\extra_collection\electronics\chris-ried-bN5XdU-bap4-unsplash.jpg")
    # main_embedding(r"D:\images\extra_collection\electronics\chris-ried-bN5XdU-bap4-unsplash.jpg")
    main_ssim(r"D:\images\extra_collection\electronics\chris-ried-bN5XdU-bap4-unsplash.jpg")


database.close_test_pictures_connection(conn)

