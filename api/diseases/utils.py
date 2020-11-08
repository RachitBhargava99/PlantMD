from tensorflow import keras
from keras_preprocessing import image
import numpy as np
from PIL import Image
from sqlalchemy.orm import Session

from typing import Tuple
import csv

from api.diseases.controllers import create_disease, get_disease_by_id
from api.symptoms.controllers import create_symptom, create_symptom_disease_link
from db import schemas
from db.db import get_db


def predict_disease_image(db: Session, pil_img: Image.Image, target_size: Tuple[int, int] = (224, 224)):
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
    li = [('Apple___Apple_scab', 605395490686926849), ('Apple___Black_rot', 605395490974105601), ('Apple___Cedar_apple_rust', 605395491135815681), ('Apple___healthy', 0),
          ('Blueberry___healthy', 0), ('Cherry_(including_sour)___Powdery_mildew', 605395492691083265), ('Cherry_(including_sour)___healthy', 0),
          ('Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 605395492809768961 ), ('Corn_(maize)___Common_rust_', 605395492997136385),
          ('Corn_(maize)___Northern_Leaf_Blight', 605395493160648705), ('Corn_(maize)___healthy', 0), ('Grape___Black_rot', 605395493319835649),
          ('Grape___Esca_(Black_Measles)', 605395493442846721), ('Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 605395493591482369), ('Grape___healthy', 0),
          ('Orange___Haunglongbing_(Citrus_greening)', 605395493682774017), ('Peach___Bacterial_spot', 605395493682774017), ('Peach___healthy', 0),
          ('Pepper,_bell___Bacterial_spot', 605395493964349441), ('Pepper,_bell___healthy', 0), ('Potato___Early_blight', 605395494098272257), ('Potato___Late_blight', 605395494264963073),
          ('Potato___healthy', 0), ('Raspberry___healthy', 0), ('Soybean___healthy', 0), ('Squash___Powdery_mildew', 605395494433554433),
          ('Strawberry___Leaf_scorch', 605395494614106113), ('Strawberry___healthy', 0), ('Tomato___Bacterial_spot', 605395492516495361), ('Tomato___Early_blight', 605395492351705089),
          ('Tomato___Late_blight', 605395492193107969), ('Tomato___Leaf_Mold', 605395492051320833), ('Tomato___Septoria_leaf_spot', 605395491909533697),
          ('Tomato___Spider_mites Two-spotted_spider_mite', 605395491764928513), ('Tomato___Target_Spot', 605395491592667137),
          ('Tomato___Tomato_Yellow_Leaf_Curl_Virus', 605395491446816769), ('Tomato___Tomato_mosaic_virus', 605395491307290625), ('Tomato___healthy', 0)]
    li = [(x.replace('___', ' - ').replace('_', ' '), str(y)) for x, y in li]
    for index, item in enumerate(d):
        if item == j:
            if li[index][1] == '0':
                return li[index][0], None
            else:
                return li[index][0], get_disease_by_id(db, int(li[index][1]))


def db_populate(db: Session, file_path: str):
    # db = get_db()
    with open(file_path, encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for curr_row in reader:
            disease = create_disease(db, schemas.DiseaseCreate(name=curr_row['name'],
                                                               scientific_name=curr_row['scientific_name'],
                                                               fruit=curr_row['fruit'],
                                                               natural_solution=curr_row['natural_solution'],
                                                               chemical_solution=curr_row['chemical_solution'],
                                                               external_link=curr_row['external_link']))
            symptoms = []
            if curr_row.get('symptom1') is not None and curr_row['symptom1'] != '':
                symptoms.append(create_symptom(db, schemas.SymptomCreate(name=curr_row['symptom1'],
                                                                         affected_part=curr_row['affected_part1']),
                                               internal=True))
            if curr_row.get('symptom2') is not None and curr_row['symptom2'] != '':
                symptoms.append(create_symptom(db, schemas.SymptomCreate(name=curr_row['symptom2'],
                                                                         affected_part=curr_row['affected_part2']),
                                               internal=True))
            if curr_row.get('symptom3') is not None and curr_row['symptom3'] != '':
                symptoms.append(create_symptom(db, schemas.SymptomCreate(name=curr_row['symptom3'],
                                                                         affected_part=curr_row['affected_part3']),
                                               internal=True))
            if curr_row.get('symptom4') is not None and curr_row['symptom4'] != '':
                symptoms.append(create_symptom(db, schemas.SymptomCreate(name=curr_row['symptom4'],
                                                                         affected_part=curr_row['affected_part4']),
                                               internal=True))
            for curr_symptom in symptoms:
                create_symptom_disease_link(db, schemas.SymptomDiseaseLinkCreate(disease_id=disease.id,
                                                                                 symptom_id=curr_symptom.id))


if __name__ == '__main__':
    db_populate('data/plantdb.csv')
