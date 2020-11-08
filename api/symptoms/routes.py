from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db import schemas
from db.db import get_db
from .controllers import create_symptom, create_symptom_disease_link, get_diseases_from_symptoms

router = APIRouter()


@router.put('', response_model=schemas.Symptom, tags=['symptom'])
def create_symptoms_route(symptom: schemas.SymptomCreate, db: Session = Depends(get_db)):
    return create_symptom(db, symptom)


@router.post('', response_model=schemas.SymptomDiseaseLink, tags=['symptom'])
def link_symptom_with_disease(sd_link: schemas.SymptomDiseaseLinkCreate, db: Session = Depends(get_db)):
    return create_symptom_disease_link(db, sd_link)


@router.post('/guess', response_model=schemas.DiseaseList, tags=['symptom'])
def guess_disease_from_symptoms(symptom_list: schemas.SymptomListWithFruit, db: Session = Depends(get_db)):
    return {'diseases': get_diseases_from_symptoms(db, symptom_list)}
