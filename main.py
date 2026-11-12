# from fastapi import Depends, FastAPI, HTTPException
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from datetime import datetime, timedelta, timezone
# import bcrypt
# import jwt

# # If using a real database, uncomment these:
# # from sqlalchemy.orm import Session
# # from db import db_session, get_user_by_username 

# from model import Token

# app = FastAPI(title="Mastering FastAPI App", description="Building with fastapi and deploy with docker")

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# SECRET_KEY = "myseccretkey"
# ALGORITHM = "HS256"

# # ==================== SECURITY UTILITIES ====================

# def hash_password(password: str) -> str:
#     password_bytes = password.encode("utf-8")
#     salt = bcrypt.gensalt()
#     hashed_bytes = bcrypt.hashpw(password_bytes, salt)
#     return hashed_bytes.decode("utf-8")

# # FIXED: Corrected "utf-8s" encoding typo and argument shadowing
# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
 
# def create_access_token(data: dict, expire_delta: timedelta = timedelta(minutes=15)) -> str:
#     to_encode = data.copy()
#     expire = datetime.now(timezone.utc) + expire_delta
#     to_encode.update({"exp": expire})
#     return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# # ==================== MOCK DATA MANAGEMENT ====================

# fake_users_db = {
#     "xyz": {  # Keyed by the actual username string for straightforward lookups
#         "username": "xyz",
#         "password": hash_password("REK!2345")
#     }
# }

# # ==================== ROUTING ENDPOINTS ====================

# @app.post("/token", response_model=Token)
# async def login_to_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
#     # OPTION A: If using your mock dictionary framework:
#     user = fake_users_db.get(form_data.username)

#     # OPTION B: If using your real SQLAlchemy database module, use this instead:
#     # (Requires injecting 'db: Session = Depends(db_session)' into the endpoint function)
#     # user = get_user_by_username(db, form_data.username)

#     # Verify user existence and password authenticity
#     # (If using option B, swap user["password"] to user.password object property)
#     if not user or not verify_password(form_data.password, user["password"]):
#         raise HTTPException(
#             status_code=401,
#             detail="Invalid credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )

#     access_token = create_access_token(data={"sub": form_data.username})
#     return {"access_token": access_token, "token_type": "bearer"}
    
# def get_current_user(token: str = Depends(oauth2_scheme)):
#     credential_exception = HTTPException(
#         status_code=401,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"}
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credential_exception
#         return username
#     except jwt.PyJWTError:
#         raise credential_exception

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
import bcrypt
import jwt

# If using a real database, uncomment these:
# from sqlalchemy.orm import Session
# from db import db_session, get_user_by_username 

from model import Token

app = FastAPI(title="Mastering FastAPI App", description="Building with fastapi and deploy with docker")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "myseccretkey"
ALGORITHM = "HS256"

# ==================== SECURITY UTILITIES ====================

def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)
    return hashed_bytes.decode("utf-8")

# FIXED: Corrected "utf-8s" encoding typo and argument shadowing
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
 
def create_access_token(data: dict, expire_delta: timedelta = timedelta(minutes=15)) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expire_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# ==================== MOCK DATA MANAGEMENT ====================

fake_users_db = {
    "xyz": {  # Keyed by the actual username string for straightforward lookups
        "username": "xyz",
        "password": hash_password("REK!2345")
    }
}

# ==================== ROUTING ENDPOINTS ====================

@app.post("/token", response_model=Token)
async def login_to_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # OPTION A: If using your mock dictionary framework:
    user = fake_users_db.get(form_data.username)

    # OPTION B: If using your real SQLAlchemy database module, use this instead:
    # (Requires injecting 'db: Session = Depends(db_session)' into the endpoint function)
    # user = get_user_by_username(db, form_data.username)

    # Verify user existence and password authenticity
    # (If using option B, swap user["password"] to user.password object property)
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}
    
def get_current_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception
        return username
    except jwt.PyJWTError:
        raise credential_exception

