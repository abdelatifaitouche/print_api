from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base , sessionmaker

DATABASE_URL = "sqlite:///test_db.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False , autoflush=False , bind=engine)


BASE = declarative_base()



def get_db():
    db = SessionLocal()
    try : 
        yield db
    finally:
        db.close()
