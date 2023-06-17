import cv2
import numpy as np
import os
import sys
from colour import calculate_histogram
import database

ordner_path = r"C:\Users\Ismai\OneDrive\Desktop\Big Data Dateien\train2017"
conn = connect_test_database()

# generator um alle Bilder mit ihren Eigenschaften in die database zu laden
def test_generator():

    #cur_img ist der Pfad zum aktuellen Bild, welcher im Generator dran ist.
    cur_img = next(img_gen)
    cur_transformed_img = cv2.imread(cur_img)
    hist = calculate_histogram(cur_transformed_img)

    cur_id = next(id_gen)
    add_test_picture(conn, cur_id, hist)

    # Dieser ganze Codeblock sorgt dafür, dass der Name des Bildes zur ID wird, wie die in der Datenbank.
    file_extension = os.path.splitext(os.path.basename(cur_img))[1]  # Dateierweiterung extrahieren
    new_filename = f"{cur_id}{file_extension}"

    old_path = os.path.join(ordner_path, os.path.basename(cur_img))
    new_path = os.path.join(ordner_path, new_filename)

    os.rename(old_path, new_path)

    print(f"Umbenannt: {old_path} -> {new_path}")

    yield cur_id

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
    pass

img_gen = image_generator(ordner_path)
id_gen = id_generator()

test = test_generator()

for i in range(100):
    next(test)

close_test_pictures_connection(conn)