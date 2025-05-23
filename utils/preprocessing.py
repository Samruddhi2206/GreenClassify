from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image

def preprocess_image(img: Image.Image, target_size=(128, 128)):
    """
    Resize, normalize, and prepare the image for prediction.

    Args:
        img (PIL.Image): The input image.
        target_size (tuple): Desired image size (width, height).

    Returns:
        numpy.ndarray: Preprocessed image array ready for model input.
    """
    img = img.resize(target_size)
    img_array = image.img_to_array(img)
    img_array = img_array / 255.0  # Normalize pixels to [0,1]
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    return img_array
