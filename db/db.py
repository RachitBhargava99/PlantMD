from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# SQLALCHEMY_DATABASE_URL = (
#         'mysql+pymysql://{user}:{password}@localhost/{database}?unix_socket=/cloudsql/{connection_name}').format(
#         user='root', password='password',
#         connection_name='thinger:us-east1:plantmd')

SQLALCHEMY_DATABASE_URL = 'cockroachdb://{username}:{password}@{hostname}:{port}/{db_name}?sslmode=disable'.format(
    username='root', password='', hostname='127.0.0.1', port='52436', db_name='plant_sql')

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
