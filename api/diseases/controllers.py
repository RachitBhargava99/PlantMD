from sqlalchemy.orm import Session

from datetime import datetime
from typing import List, Union

from db import models, schemas


def _create_fruit_if_not_exists(db: Session, fruit_name: str) -> None:
    db_fruit = db.query(models.Fruit).filter_by(name=fruit_name).first()
    if db_fruit is None:
        db_fruit = models.Fruit(name=fruit_name)
        db.add(db_fruit)
        db.commit()


def create_disease(db: Session, disease: schemas.DiseaseCreate) -> schemas.Disease:
    _create_fruit_if_not_exists(db, disease.fruit)
    db_disease = models.Disease(name=disease.name, scientific_name=disease.scientific_name, fruit=disease.fruit,
                                natural_solution=disease.natural_solution, chemical_solution=disease.chemical_solution,
                                external_link=disease.external_link)
    db.add(db_disease)
    db.commit()
    db.refresh(db_disease)
    return db_disease


def get_disease_by_name_and_fruit(db: Session, disease_name: str, fruit_name: str) -> schemas.Disease:
    return db.query(models.Disease).filter_by(name=disease_name, fruit=fruit_name).first()


def get_disease_by_id(db: Session, disease_id: int) -> schemas.Disease:
    return db.query(models.Disease).filter_by(id=disease_id).first()


def create_symptom(db: Session, symptom: schemas.SymptomCreate) -> schemas.Symptom:
    db_symptom = models.Symptom(name=symptom.name, affected_part=symptom.affected_part)
    db.add(db_symptom)
    db.commit()
    db.refresh(db_symptom)
    return db_symptom


def create_symptom_disease_link(db: Session, sd_link: schemas.SymptomDiseaseLinkCreate) -> schemas.SymptomDiseaseLink:
    db_link = models.SymptomDiseaseLink(disease_id=sd_link.disease_id, symptom_id=sd_link.symptom_id)
    db.add(db_link)
    db.commit()
    db.refresh(db_link)
    return db_link

#soph experimenting space :)
def get_disease_by_fruit(db: Session, fruit_name: str):
    db_link = db.query(models.Disease).filter_by(fruit = fruit_name)
    return [x for x in db_link]

def get_symptoms_by_disease(db: Session, disease_id: int):
    db_link = db.query(models.SymptomDiseaseLink).filter_by(disease_id=disease_id)
    symptoms = []
    for link in db_link:
        symptoms.append(db.query(models.Symptom).filter_by(id=link.symptom_id).first())
    return symptoms