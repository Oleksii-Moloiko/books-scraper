from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, autoincrement=True)

    product_url = Column(String(250), nullable=False, unique=True)  # NEW

    img_url = Column(String(250), nullable=False)
    rating = Column(Integer, nullable=False)
    title = Column(String(150), nullable=False)  # без unique
    price = Column(Float, nullable=False)
    created = Column(DateTime, default=datetime.now)
