import cv2
import numpy as np
import os
import sys
from colour import calculate_histogram
from colour import bhattacharyya_distance
import database
import pandas as pd
import csv
import pickle
import heapq
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

ordner_path = r"C:\Users\Ismai\OneDrive\Desktop\Big Data Dateien\train2017"
conn = database.connect_test_database()

hist_data = []


# function to fill path database and histogram with id into list hist_data
def data(img_gen, id_gen):

    cur_img = next(img_gen)
    cur_transformed_img = cv2.imread(cur_img)
    hist = calculate_histogram(cur_transformed_img)
    # print(hist)
    cur_id = next(id_gen)
    hist_data.append([cur_id, hist])
    database.add_path(conn, cur_id, cur_img)


# transform the csv file into pickle file
def data_to_pickle():
    df = pd.DataFrame(hist_data, columns=['Id', 'Histogram'])
    df.to_pickle("histograms.pkl")


# load the pickel file as df_restored
def read_pickle():
    df_restored = pd.read_pickle("histograms.pkl")
    return df_restored


def id_generator():
    current_id = 1
    while True:
        yield current_id
        current_id += 1


def image_generator(path):
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif']  # Liste der unterstützten Bildformate

    for filename in os.listdir(path):
        file_extension = os.path.splitext(filename)[1].lower()  # Dateierweiterung in Kleinbuchstaben extrahieren
        if file_extension in image_extensions:
            yield os.path.join(path, filename)


# gitb die top five der jeweiligen kategorie aus
def topfive(dict):
    largest_values = heapq.nlargest(5, dict, key=dict.get)

    return largest_values


# generator um das input-Bild mit allen Bildern in der Datenbank zu vergleichen
def generator_vergleich(input_img):
    new_img = cv2.imread(input_img)
    new_hist = calculate_histogram(new_img)

    # ÄNDERN, sortieren o.ä
    compare_dict = {}
    df = read_pickle()
    for index, row in df.iterrows():
        cur_id = row["Id"]
        cur_hist = row["Histogram"]
        compare_dict[cur_id] = bhattacharyya_distance(new_hist, cur_hist)

    return compare_dict


# soll die topfive bilder darstellen, finaler output
def zeige_bilder(conn, top_five_list, dict):
    path_liste = []
    for id in top_five_list:
        path_liste.append(database.get_path_from_id(conn, id))

    fig, axes = plt.subplots(nrows=1, ncols=5, figsize=(12, 4))

    # Bilder laden und anzeigen
    for i in range(5):
        image_path = path_liste[i]
        image = mpimg.imread(image_path)
        axes[i].imshow(image)
        axes[i].axis('off')

        fig.text(0.5, 0.95, 'Farbschema', fontsize=12, color='white', backgroundcolor="black", weight="bold",
                  ha='center', va='center')
        text = f"{round(dict[top_five_list[i]],2)*100}% Ähnlichkeit"
        axes[i].text(0, 0, text, color='white', backgroundcolor='black', fontsize=10, weight='bold')

    # Bilder anzeigen
    plt.tight_layout()
    plt.show()




# soll alles verbinden
def data_ready():

    database.reset_database(conn)

    database.create_path_table(conn)

    img_gen = image_generator(ordner_path)
    id_gen = id_generator()

    for i in range(31000):
        data(img_gen, id_gen)

    data_to_pickle()


def main(input_image):

    dict = generator_vergleich(input_image)

    top_five = topfive(dict)

    image = mpimg.imread(input_image)

    # Figur erstellen
    fig2 = plt.figure()

    plt.imshow(image)
    fig2.text(0.5, 0.95, 'Input Image', fontsize=12, color='red', backgroundcolor="black",weight="bold", ha='center', va='center')
    plt.axis('off')

    plt.show(block=False)

    zeige_bilder(conn, top_five, dict)

main(r"C:\Users\Ismai\Downloads\tempxwiesebluehengjpg100~_v-gseagaleriexl.jpg")


database.close_test_pictures_connection(conn)

