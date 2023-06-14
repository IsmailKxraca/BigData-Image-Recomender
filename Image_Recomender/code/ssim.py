import numpy as np
from skimage import io, metrics, transform

# Load the images
image1 = io.imread('Unbenannt.jpg', as_gray=True)
image2 = io.imread('Unbenannt2.jpg', as_gray=True)

# Resize the images to have the same dimensions
image1 = transform.resize(image1, image2.shape, mode='reflect')

# Calculate the SSIM
ssim_score = metrics.structural_similarity(image1, image2)

# Print the SSIM score
print("SSIM:", ssim_score)