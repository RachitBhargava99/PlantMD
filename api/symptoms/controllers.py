from sqlalchemy.orm import Session

from typing import List

from db import models, schemas


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


def get_all_diseases_by_fruit(db: Session, fruit_name: str) -> List[schemas.Disease]:
    db_diseases = db.query(models.Disease).filter_by(fruit=fruit_name)
    return [x for x in db_diseases]


def get_diseases_from_symptoms(db: Session, symptom_list: schemas.SymptomListWithFruit) -> List[schemas.Disease]:
    disease_list = get_all_diseases_by_fruit(db, symptom_list.fruit)
    for curr_symptom_id in symptom_list.symptoms:
        print(symptom_list.symptoms)
        curr_rel_links = db.query(models.SymptomDiseaseLink).filter_by(symptom_id=curr_symptom_id)
        curr_rel_ids = [x.symptom_id for x in curr_rel_links]
        disease_list = [x for x in disease_list if x.id in curr_rel_ids]
    return disease_list
