from tensorflow import keras
from keras_preprocessing import image
import numpy as np
from PIL import Image

from typing import Tuple


def predict_disease_image(pil_img: Image.Image, target_size: Tuple[int, int] = (224, 224)):
    model = keras.models.load_model('models/AlexNetModel.hdf5')
    pil_img = pil_img.convert('RGB')
    width_height_tuple = (target_size[1], target_size[0])
    if pil_img.size != width_height_tuple:
        pil_img = pil_img.resize(width_height_tuple, Image.NEAREST)
    # print(pil_img)
    # new_img = image.load_img('AppleCedarRust2.jpg', target_size=(224, 224))
    img = image.img_to_array(pil_img)
    img = np.expand_dims(img, axis=0)
    img = img / 255
    prediction = model.predict(img)
    # print(prediction)
    d = prediction.flatten()
    j = d.max()
    li = ['Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy',
          'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew', 'Cherry_(including_sour)___healthy',
          'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 'Corn_(maize)___Common_rust_',
          'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy', 'Grape___Black_rot',
          'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Grape___healthy',
          'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot', 'Peach___healthy',
          'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 'Potato___Early_blight', 'Potato___Late_blight',
          'Potato___healthy', 'Raspberry___healthy', 'Soybean___healthy', 'Squash___Powdery_mildew',
          'Strawberry___Leaf_scorch', 'Strawberry___healthy', 'Tomato___Bacterial_spot', 'Tomato___Early_blight',
          'Tomato___Late_blight', 'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot',
          'Tomato___Spider_mites Two-spotted_spider_mite', 'Tomato___Target_Spot',
          'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus', 'Tomato___healthy']
    li = [x.replace('___', ' - ').replace('_', ' ') for x in li]
    for index, item in enumerate(d):
        if item == j:
            return li[index]
