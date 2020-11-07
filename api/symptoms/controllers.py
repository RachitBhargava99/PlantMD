from sqlalchemy.orm import Session

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
