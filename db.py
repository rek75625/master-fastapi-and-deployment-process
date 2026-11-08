from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from .model import User

Base = declarative_base()

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def create_user(db: Session, username: str, email: str):
    user  = User(username=username,email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_username(db: Session,username : str):
    return db.query(User).filter(User.username == username).first()

def update_user_email(db:Session,user_id:int, new_email:str):
    db_user = db.query(User).filter(User.id==id).first()
    if db_user:
        db.query(User).filter(User.id==id).update(values={db_user.email:new_email})
        db_user.email=new_email
        db.commit()
        db.refresh(db_user)
        return db_user
    
def delete_user(db: Session,user_id:int):
    db_user = db.query(User).filter(User.id==id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user