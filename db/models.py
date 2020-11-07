from sqlalchemy import Column, Integer, String, ForeignKey

from .db import Base


class Fruit(Base):
    __tablename__ = 'fruits'

    name = Column(String(63), primary_key=True)


class Disease(Base):
    __tablename__ = 'diseases'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(63))
    scientific_name = Column(String(127))
    fruit = Column(String(63), ForeignKey('fruits.name'))


class Symptom(Base):
    __tablename__ = 'symptoms'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(63))
    affected_part = Column(String(31))


class SymptomDiseaseLink(Base):
    __tablename__ = 'symptom_disease_links'

    disease_id = Column(Integer, ForeignKey('diseases.id'))
    symptom_id = Column(Integer, ForeignKey('symptoms.id'))
