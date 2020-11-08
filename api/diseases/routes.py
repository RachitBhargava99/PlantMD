from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from PIL import Image

from io import BytesIO
import base64

from db import schemas
from db.db import get_db
from .controllers import create_disease, create_symptom, create_symptom_disease_link, get_disease_by_id, get_disease_by_fruit, get_symptoms_by_disease
from .utils import predict_disease_image

router = APIRouter()


@router.put('', response_model=schemas.Disease)
def create_plant_disease(disease: schemas.DiseaseCreate, db: Session = Depends(get_db)):
    return create_disease(db, disease)


@router.get('/{disease_id}', response_model=schemas.Disease)
def create_plant_disease(disease_id: int, db: Session = Depends(get_db)):
    return get_disease_by_id(db, disease_id)


@router.put('/symptom', response_model=schemas.Symptom)
def create_symptoms_route(symptom: schemas.SymptomCreate, db: Session = Depends(get_db)):
    return create_symptom(db, symptom)


@router.post('/symptom', response_model=schemas.SymptomDiseaseLink)
def link_symptom_with_disease(sd_link: schemas.SymptomDiseaseLinkCreate, db: Session = Depends(get_db)):
    return create_symptom_disease_link(db, sd_link)


@router.post('/image')
def predict_disease_from_image(image: schemas.ImageInput):
    pil_img = Image.open(BytesIO(base64.b64decode(image.b64_img)))
    return {'prediction': predict_disease_image(pil_img)}

#soph experimenting space :)

@router.get('/symptom')
def get_symptoms_from_fruit(fruit: schemas.FruitInput, db: Session = Depends(get_db)):
    dList = get_disease_by_fruit(db, fruit.name)
    sList = []
    for disease in dList:
        sList.extend(get_symptoms_by_disease(db, disease.id))
    sList = list(set(sList))
    return {'symptoms': sList}