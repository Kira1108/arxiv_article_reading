from sqlalchemy import Column, Integer, String, Table,DateTime
from database import SuperBase

def create_article_meta(superbase:SuperBase):
    class ArticleMeta(superbase.Base):
        __tablename__ = "article_meta"
        id:int = Column(Integer, primary_key=True, index=True)
        entry_id:str = Column(String, unique=True, nullable=False)
        updated: str = Column(DateTime, nullable=True)
        published: str = Column(DateTime, nullable=True)
        title: str = Column(String, nullable=True)
        authors: str = Column(String, nullable=True)
        summary: str = Column(String, nullable=True)
        comment: str = Column(String, nullable=True)
        journal_ref: str = Column(String, nullable=True)
        doi: str = Column(String, nullable=True)
        primary_category: str = Column(String, nullable=True)
        categories: str = Column(String, nullable=True)
        links: str = Column(String, nullable=True)
        pdf_url: str = Column(String, nullable=True)
        pdf_path:str = Column(String, nullable=True)
    return ArticleMeta

class ArticleCrud:
    def __init__(self, superbase:SuperBase, table:Table):
        self.superbase = superbase
        self.table = table 

    def get_db(self):
        return next(self.superbase.get_db())

    def create(self, obj):
        db = self.get_db()
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj
    
    def get_by_entry_id(self,entry_id):
        db = self.get_db()
        return db.query(self.table).filter(self.table.entry_id == entry_id).first()
    
    def get_by_id(self, id):
        db = self.get_db()
        return db.query(self.table).filter(self.table.id == id).first()
    
    def get_all(self):
        db = self.get_db()
        return db.query(self.table).all()
    
    def delete_by_id(self,id):
        db = self.get_db()
        db.query(self.table).filter(self.table.id == id).delete()
        db.commit()
        return True
    
    def delete_by_entry_id(self, entry_id):
        db = self.get_db()
        db.query(self.table).filter(self.table.entry_id == entry_id).delete()
        db.commit()
        return True

