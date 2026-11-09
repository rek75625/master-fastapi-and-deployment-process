from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm import Session, sessionmaker
from .model import User
from fastapi import HTTPException

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
    try:
        user  = User(username=username,email=email)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError:
        db.rollback()
        HTTPException(status_code=400, detail="User with this username or email already exists")
        
def get_user_by_username(db: Session,username : str):
    return db.query(User).filter(User.username == username).first()

def update_user_email(db:Session,user_id:int, new_email:str):
    try:
        db_user = db.query(User).filter(User.id==user_id).first()
        if not db_user:
            ValueError("User not found")
            # db.query(User).filter(User.id==user_id).update(values={db_user.email:new_email})
            db_user.email=new_email
            db.commit()
            db.refresh(db_user)
            return db_user
    except Exception as e:
        db.rollback()
        HTTPException(status_code=404,detail=str(e))
        
    
def delete_user(db: Session,user_id:int):
    db_user = db.query(User).filter(User.id==id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user