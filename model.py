# from sqlalchemy.orm import declarative_base
# from sqlalchemy import Column, Integer, String
# from pydantic import BaseModel, EmailStr

# # Create the base class that SQLAlchemy uses to track tables
# Base = declarative_base()

# class User(Base):
#     __tablename__ = "users"
    
#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String, unique=True, index=True)
#     email = Column(String, unique=True, index=True)


# # What the API expects when a new client creates a user account
# class UserCreate(BaseModel):
#     username: str
#     email: EmailStr

# # What the API sends back to the client (includes the database ID)
# class UserResponse(BaseModel):
#     id: int
#     username: str
#     email: EmailStr

#     class Config:
#         from_attributes = True  # Tells Pydantic to read data safely from SQLAlchemy objects

# # Model to represent the token received after authentication
# class Token(BaseModel):
#     access_token: str
#     token_type: str

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
from pydantic import BaseModel, EmailStr

# Create the base class that SQLAlchemy uses to track tables
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)


# What the API expects when a new client creates a user account
class UserCreate(BaseModel):
    username: str
    email: EmailStr

# What the API sends back to the client (includes the database ID)
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True  # Tells Pydantic to read data safely from SQLAlchemy objects

# Model to represent the token received after authentication
class Token(BaseModel):
    access_token: str
    token_type: str

