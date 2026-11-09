from pydantic import BaseModel
from sqlalchemy import Column, Integer, String

from main import Base

class User(BaseModel):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    
# Model to represent the token received after authentication
class Token(BaseModel):
    access_token: str
    token_type: str
