from sqlalchemy.orm import Session
from fastapi import HTTPException

from typing import List

from db import models, schemas


def get_symptom_by_name_and_affected_part(db: Session, name: str, affected_part: str) -> schemas.Symptom:
    return db.query(models.Symptom).filter_by(name=name, affected_part=affected_part).first()


def create_symptom(db: Session, symptom: schemas.SymptomCreate, internal: bool = False) -> schemas.Symptom:
    pre_symptom = get_symptom_by_name_and_affected_part(db, symptom.name, symptom.affected_part)
    if pre_symptom is not None:
        if internal:
            return pre_symptom
        raise HTTPException(status_code=409,
                            detail="The provided symptom already exists. " +
                                   "Please use that instead of creating a new one.")
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


def get_all_diseases_by_fruit(db: Session, fruit_name: str) -> List[schemas.Disease]:
    db_diseases = db.query(models.Disease).filter_by(fruit=fruit_name)
    return [x for x in db_diseases]


def get_diseases_from_symptoms(db: Session, symptom_list: schemas.SymptomListWithFruit) -> List[schemas.Disease]:
    disease_list = get_all_diseases_by_fruit(db, symptom_list.fruit)
    print(symptom_list.symptoms)
    for curr_symptom_id in symptom_list.symptoms:
        curr_rel_links = db.query(models.SymptomDiseaseLink).filter_by(symptom_id=curr_symptom_id)
        curr_rel_ids = [x.disease_id for x in curr_rel_links]
        print(curr_rel_ids)
        disease_list = [x for x in disease_list if x.id in curr_rel_ids]
    return disease_list


def get_disease_by_fruit(db: Session, fruit_name: str):
    db_link = db.query(models.Disease).filter_by(fruit=fruit_name)
    return [x for x in db_link]


def get_symptoms_by_disease(db: Session, disease_id: int):
    db_link = db.query(models.SymptomDiseaseLink).filter_by(disease_id=disease_id)
    symptoms = []
    for link in db_link:
        curr_symp = db.query(models.Symptom).filter_by(id=link.symptom_id).first()
        curr_symp.id = str(curr_symp.id)
        symptoms.append(curr_symp)
    return symptoms


def get_all_symptoms(db: Session):
    all_symptoms = [x for x in db.query(models.Symptom).all()]
    for curr_symptom in all_symptoms:
        curr_symptom.id = str(curr_symptom.id)
    return all_symptoms
