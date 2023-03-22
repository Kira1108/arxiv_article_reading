from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from dataclasses import dataclass
import os
import logging
logger = logging.getLogger("uvicorn")

DATABASE_FOLDER = "./databases"

@dataclass
class SuperBase:
    """Create Database Dynamically"""
    name:str
    folder:str = DATABASE_FOLDER

    def __post_init__(self):
        os.makedirs(self.folder, exist_ok=True)
        self.db_uri = f"sqlite:///{self.folder}/{self.name}.db"
        self.engine = create_engine(self.db_uri)
        self.session_local = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine)
        self.Base = declarative_base()
        
    def get_db(self):
        db = self.session_local()
        try:
            yield db
        finally:
            db.close()
    
if __name__ == "__main__":
    superdb = SuperBase("test")

    class SomeTable(superdb.Base):
        __tablename__ = "some_table"
        id = Column(Integer, primary_key=True, index=True)
        name = Column(String, unique=True, index=True, nullable=False)
        description = Column(String, nullable=True)

    superdb.Base.metadata.create_all(bind=superdb.engine)