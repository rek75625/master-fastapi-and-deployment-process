from fastapi import Depends, FastAPI, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
import bcrypt
import jwt

from db import get_user_by_username
from model import Token
# from sqlalchemy.orm import Session
# from .db import create_user, db_session, get_user_by_username, update_user_email
# from .model import User
app = FastAPI(title="Mastering FastAPI App", description="Building with fastapi and deploy with docker")
# Set up the oauth to paswwrod properly (using token)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "myseccretkey"
ALGORITHM = "HS256"


# Clean, native bcrypt implementation
def hash_password(password: str) -> str:
    # Convert password string to bytes
    password_bytes = password.encode("utf-8")
    # Generate salt and hash
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)
    # Decode back to a string to store in the database
    return hashed_bytes.decode("utf-8")

def verify_password(plain_password: str,hash_password:str)-> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"),hash_password.encode("utf-8s"))
 
# Now we create a token by using create access token function
from datetime import datetime, timedelta, timezone
import jwt

# Configuration (Ensure these match your global variables)
SECRET_KEY = "myseccretkey"
ALGORITHM = "HS256"


# Now we create a token by using create access token function
def create_access_token(
    data: dict, expire_delta: timedelta = timedelta(minutes=15)
) -> str:
    to_encode = data.copy()

    # Use modern timezone-aware UTC datetime instead of utcnow()
    expire = datetime.now(timezone.utc) + expire_delta

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


fake_users_db = {
    "check-name":{
        "username":"xyz",
        "password":hash_password("REK!2345")
    }
}

@app.post("/token", response_model=Token)
async def login_to_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    # Fetch user from mock database
    user = get_user_by_username(fake_users_db, form_data.username)

    # Verify user existence and password authenticity
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generate token using username as the Subject identifier ('sub')
    access_token = create_access_token(data={"sub": form_data.username})

    return {"access_token": access_token, "token_type": "bearer"}
    
def get_current_user(token:str=Depends(oauth2_scheme)):
    credential_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate":"Bearer"}
    )
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception
        return username
    except jwt.PyJWTError:
        raise credential_exception 


