from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from db import schemas
from db.db import get_db
from .controllers import create_disease, create_symptom, create_symptom_disease_link

router = APIRouter()


@router.put('', response_model=schemas.Disease)
def create_plant_disease(disease: schemas.DiseaseCreate, db: Session = Depends(get_db)):
    return create_disease(db, disease)


@router.put('/symptom', response_model=schemas.Symptom)
def create_symptoms_route(symptom: schemas.SymptomCreate, db: Session = Depends(get_db)):
    return create_symptom(db, symptom)


@router.post('/symptom', response_model=schemas.SymptomDiseaseLink)
def link_symptom_with_disease(sd_link: schemas.SymptomDiseaseLinkCreate, db: Session = Depends(get_db)):
    return create_symptom_disease_link(db, sd_link)
