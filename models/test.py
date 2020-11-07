from tensorflow import keras
from keras_preprocessing import image
import numpy as np

if __name__ == '__main__':
    model = keras.models.load_model('AlexNetModel.hdf5')
    new_img = image.load_img('AppleCedarRust2.jpg', target_size=(224, 224))
    img = image.img_to_array(new_img)
    img = np.expand_dims(img, axis=0)
    img = img / 255
    print(model.predict(img))
