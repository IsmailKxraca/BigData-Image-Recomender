import cv2
import numpy as np
import os
import sys
from colour import calculate_histogram
from colour import bhattacharyya_distance
import database
import pandas as pd
import pickle
import heapq
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# our path with the image data
ordner_path = r"C:\Users\Ismai\OneDrive\Desktop\Big Data Dateien\train2017"
conn = database.connect_test_database()

# the list where we save the ID + Histograms temporarily
hist_data = []
ssim_data = []


# function to fill path database and histogram with id into list hist_data
def data(img_gen, id_gen):

    cur_img = next(img_gen)
    cur_transformed_img = cv2.imread(cur_img)

    hist = calculate_histogram(cur_transformed_img)

    resized_image = cv2.resize(image, (128, 128))
    gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
    ssim = np.reshape(gray_image, (128 * 128))

    # print(hist)
    cur_id = next(id_gen)
    hist_data.append([cur_id, hist])
    ssim_data.append([cur_id, ssim])
    database.add_path(conn, cur_id, cur_img)


# loads the hist_data list into a Dataframe and than turns it into a pickle file
def data_to_pickle():
    df = pd.DataFrame(hist_data, columns=['Id', 'Histogram'])
    df.to_pickle("histograms.pkl")

    df_ssim = pd.pd.DataFrame(hist_data, columns=['Id', 'Ssim'])
    df_ssim.to_pickle("ssim.pkl")


# load the histograms into a pickle file
def read_pickle_hist():
    df_restored = pd.read_pickle("histograms.pkl")
    return df_restored


# load the resized and grayscaled images into a pickle file
def read_pickle_ssim():
    df_restored = pd.read_pickle("ssim.pkl")
    return df_restored


# counter as generator for giving the IDs
def id_generator():
    current_id = 1
    while True:
        yield current_id
        current_id += 1


# generator giving out one picture-path per skip in the given Ordner
def image_generator(path):
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif']

    for filename in os.listdir(path):
        file_extension = os.path.splitext(filename)[1].lower()
        if file_extension in image_extensions:
            yield os.path.join(path, filename)


# input = dictionary with all similarities. Output = list with Ids of the top five highest values.
def topfive(dict):
    largest_values = heapq.nlargest(5, dict, key=dict.get)

    return largest_values


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
        text = f"{round(dict[top_five_list[i]],3)*100}% Ähnlichkeit"
        axes[i].text(0, 0, text, color='white', backgroundcolor='black', fontsize=10, weight='bold')

    # final plot
    plt.tight_layout()
    plt.show()


# plots the top five most similar images for histograms
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
        text = f"{round(dict[top_five_list[i]],3)*100}% Ähnlichkeit"
        axes[i].text(0, 0, text, color='white', backgroundcolor='black', fontsize=10, weight='bold')

    # final plot
    plt.tight_layout()
    plt.show()

# makes database + histogram pickle file ready. with the 31000 images of the Ordner
def data_ready():
    database.reset_database(conn)

    database.create_path_table(conn)

    img_gen = image_generator(ordner_path)
    id_gen = id_generator()

    for i in range(31000):
        data(img_gen, id_gen)

    data_to_pickle()


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


#data_to_pickle()
main_hist(r"C:\Users\Ismai\Downloads\tempxwiesebluehengjpg100~_v-gseagaleriexl.jpg")


database.close_test_pictures_connection(conn)

