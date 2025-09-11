from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./chatbot.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String, index=True)  # laptop, smartphone, etc.
    price = Column(Float)
    ram = Column(Integer)  # in GB
    storage = Column(Integer)  # in GB
    weight = Column(Float)  # in kg
    screen_size = Column(Float)  # in inches
    processor = Column(String)
    graphics = Column(String)
    battery_life = Column(Integer)  # in hours
    use_case = Column(String)  # education, gaming, business, etc.
    upgradable_ram = Column(Boolean, default=False)
    upgradable_storage = Column(Boolean, default=False)
    description = Column(Text)
    image_url = Column(String)
    brand = Column(String)
    
class ChatSession(Base):
    __tablename__ = "chat_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, index=True)
    memory = Column(Text)  # JSON string of slot-filling memory
    created_at = Column(String)
    updated_at = Column(String)

def create_tables():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
