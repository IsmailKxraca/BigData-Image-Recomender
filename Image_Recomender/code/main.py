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
def topfive(kategorie):
    pass


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
def zeige_bilder():
    pass


# soll alles verbinden
def main():

    database.reset_database(conn)

    database.create_path_table(conn)

    img_gen = image_generator(ordner_path)
    id_gen = id_generator()

    for i in range(1000):
        data(img_gen, id_gen)

    data_to_pickle()


main()
database.show_path(conn)

dict = generator_vergleich(r"C:\Users\Ismai\OneDrive\Desktop\train2017\000000008876.jpg")
print(dict)

database.close_test_pictures_connection(conn)

