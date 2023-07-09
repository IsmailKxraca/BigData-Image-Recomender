import cv2
import numpy as np
import os
import sys
from colour import calculate_histogram
import database
import pandas as pd
from embeddings import extract_mobilenet_features
from embeddings import calculate_euclidean_distance


# our path with the image data
ordner_path = r"D:\images"
conn = database.connect_test_database()

# the list where we save the ID + Histograms temporarily
hist_data = []
ssim_data = []
embeddings_data = []


# counter as generator for giving the IDs
def id_generator():
    current_id = 1
    while True:
        yield current_id
        current_id += 1


# generator giving out one picture-path per skip in the given Ordner
def image_generator(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                image_path = os.path.join(root, file)
                yield image_path


# function to fill the current image measures + current ID into the related Similarity-Measure-List
# adds the current image-path + ID into the database
def data(img_gen, id_gen):
    try:
        cur_img = next(img_gen)
        cur_transformed_img = cv2.imread(cur_img)

        # histograms of the images get calculated
        hist = calculate_histogram(cur_transformed_img)

        # ssim, resized and grayscaled images get saved
        resized_image = cv2.resize(cur_transformed_img, (128, 128))
        gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
        ssim = np.reshape(gray_image, (128 * 128))

        # embeddings, the feature vector of the image gets extracted
        img_features = extract_mobilenet_features(cur_img)

        cur_id = next(id_gen)

        hist_data.append([cur_id, hist])
        ssim_data.append([cur_id, ssim])
        embeddings_data.append([cur_id, img_features])

        database.add_path(conn, cur_id, cur_img)

    except cv2.error as e:
        data(img_gen, id_gen)


# loads the hist_data list into a Dataframe and than turns it into a pickle file
def data_to_pickle():
    df = pd.DataFrame(hist_data, columns=['Id', 'Histogram'])
    df.to_pickle("histograms.pkl")

    df_ssim = pd.DataFrame(ssim_data, columns=['Id', 'Ssim'])
    df_ssim.to_pickle("ssim.pkl")

    df_embeddings = pd.DataFrame(embeddings_data, columns=['Id', 'Feature_vector'])
    df_embeddings.to_pickle("embeddings.pkl")


# updates the pickle files. Attaches the new Data to the existing Data.
def pickle_update():
    df_restored_hist = pd.read_pickle("histograms.pkl")
    df_restored_ssim = pd.read_pickle("ssim.pkl")
    df_restored_embedding = pd.read_pickle("embeddings.pkl")

    df_new_hist = pd.DataFrame(hist_data,columns=['Id', 'Histogram'])
    df_new_ssim = pd.DataFrame(ssim_data,columns=['Id', 'Ssim'])
    df_new_embedding = pd.DataFrame(embeddings_data,columns=['Id', 'Feature_vector'])

    df_hist = pd.concat([df_restored_hist, df_new_hist])
    df_ssim = pd.concat([df_restored_ssim, df_new_ssim])
    df_embedding = pd.concat([df_restored_embedding, df_new_embedding])

    df_hist.to_pickle("histograms.pkl")
    df_ssim.to_pickle("ssim.pkl")
    df_embedding.to_pickle("embeddings.pkl")


# main-function. Connects everything and makes final result.
def data_ready():
    database.reset_database(conn)

    database.create_path_table(conn)

    img_gen = image_generator(ordner_path)
    id_gen = id_generator()

    for i in range(len(img_gen)):
        data(img_gen, id_gen)

    data_to_pickle()

def data_continue():
    img_gen = image_generator(ordner_path)
    id_gen = id_generator()

    for i in range(123000):
        next(img_gen)
        next(id_gen)

    for i in range(5000):
        data(img_gen, id_gen)

    pickle_update()

#data_continue()

#database.show_path(conn)
print(database.get_record_count(conn))



database.close_test_pictures_connection(conn)