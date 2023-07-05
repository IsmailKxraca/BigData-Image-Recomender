import numpy as np
from skimage import io, metrics, transform
from PIL import Image


def resize_and_convert_to_gray(image_path):
    # Bild öffnen und auf 128x128 Pixel skalieren
    image = Image.open(image_path)
    image = image.resize((128, 128), Image.ANTIALIAS)

    # Bild in Graustufen umwandeln
    gray_image = image.convert('L')

    return gray_image


# Beispielaufruf für ein Bild
image_path = r'C:\Users\Ismai\Downloads\csm_DSCN1971_54c3f433ac.jpg'
resized_gray_image = resize_and_convert_to_gray(image_path)

print(resized_gray_image)
# Beispiel: Anzeigen des skalierten und umgewandelten Bildes
resized_gray_image.show()

# Load the images
image1 = io.imread('Unbenannt.jpg', as_gray=True)
image2 = io.imread('Unbenannt2.jpg', as_gray=True)

# Resize the images to have the same dimensions
image1 = transform.resize(image1, image2.shape, mode='reflect')

# Calculate the SSIM
ssim_score = metrics.structural_similarity(image1, image2)

# Print the SSIM score
print("SSIM:", ssim_score)