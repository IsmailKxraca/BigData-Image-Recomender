from colour.py import calculate_histogram
from database.py import connect_test_database

# generator um alle Bilder mit ihren Eigenschaften in die database zu laden
def test_generator():
    pass


def id_generator():
    current_id = 1
    while True:
        yield current_id
        current_id += 1


# das input Bild muss bearbeitet werden
def input_picture_hist(image):
    hist = colour.calculate_histogram(image)
    return hist

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