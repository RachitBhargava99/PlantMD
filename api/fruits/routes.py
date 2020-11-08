from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db import schemas
from db.db import get_db
from .controllers import get_all_fruits

router = APIRouter()


@router.get('', response_model=schemas.FruitList, tags=['fruit'])
def get_fruits(db: Session = Depends(get_db)):
    return {'fruits': get_all_fruits(db)}
