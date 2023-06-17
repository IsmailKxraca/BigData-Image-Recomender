import cv2
import numpy as np
import os
import sys
from colour import calculate_histogram
import database

ordner_path = r"C:\Users\Ismai\OneDrive\Desktop\Big Data Dateien\train2017"
conn = database.connect_test_database()

# generator um alle Bilder mit ihren Eigenschaften in die database zu laden
def test_generator(img_gen, id_gen):

    #cur_img ist der Pfad zum aktuellen Bild, welcher im Generator dran ist.
    cur_img = next(img_gen)
    cur_transformed_img = cv2.imread(cur_img)
    hist = calculate_histogram(cur_transformed_img)
    print(hist)

    cur_id = next(id_gen)
    database.add_test_picture(conn, cur_id, str(hist))
    database.add_path(conn, cur_id, cur_img)

    print(f"{cur_id} successfully gespeichert")


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
def generator_vergleich():
    pass


# soll die topfive bilder darstellen, finaler output
def zeige_bilder():
    pass


# soll alles verbinden
def main():

    database.reset_database(conn)

    database.create_table(conn)
    database.create_path_table(conn)

    img_gen = image_generator(ordner_path)
    id_gen = id_generator()

    for i in range(100):
        test_generator(img_gen,id_gen)

main()

database.show_test_pictures(conn)

database.close_test_pictures_connection(conn)
