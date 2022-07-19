"Authentication"
import json
from typing import Union
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
import requests
from settings import ALGORITHM, SECRET_KEY, API_URL, API_KEY
from sqlalchemy.orm import Session
from sql_app.repositories import UserRepo
from sql_app.schemas import TokenData
from sql_app.db import get_db
from jose import JWTError, jwt


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


class TokenHandler:
    """
    Token Handler
    """
    def __init__(self):
        self.token_value = None
    @property
    def token(self):
        """
        Return token
        """
        if self.token_value is None:
            print('ZA RABOTU')
            self.token_value = requests.post(f'http://{API_URL}/api/v1/auth',
                data=json.dumps({'api_key': API_KEY})).json()['token']
        return self.token_value

def verify_password(plain_password, hashed_password):
    """
    Verify hashed password with plain password
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """
    Hash plain password
    """
    return pwd_context.hash(password)

def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
    """
    Checks if the username and password are valid
    """
    user_db = UserRepo.fetch_by_name(db=db, username=username)
    if not user_db:
        return False
    if not verify_password(password, user_db.password):
        return False
    return user_db


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    """
    Create access token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt





def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    Check if user is authenticated
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError as jwt_err:
        raise credentials_exception from jwt_err
    user = UserRepo.fetch_by_name(db=db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user
