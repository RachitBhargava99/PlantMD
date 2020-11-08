from sqlalchemy.orm import Session

from typing import List

from db import models, schemas


def get_all_fruits(db: Session) -> List[schemas.Fruit]:
    return [x for x in db.query(models.Fruit).all()]
