from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db import schemas
from db.db import get_db
from .controllers import create_symptom, create_symptom_disease_link

router = APIRouter()


@router.put('', response_model=schemas.Symptom)
def create_symptoms_route(symptom: schemas.SymptomCreate, db: Session = Depends(get_db)):
    return create_symptom(db, symptom)


@router.post('', response_model=schemas.SymptomDiseaseLink)
def link_symptom_with_disease(sd_link: schemas.SymptomDiseaseLinkCreate, db: Session = Depends(get_db)):
    return create_symptom_disease_link(db, sd_link)
