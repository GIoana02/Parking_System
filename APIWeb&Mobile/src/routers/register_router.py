from datetime import timedelta, datetime
from http.client import HTTPException

import jwt as jwt
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from src.models.user import UserRegister, UserLogin
from src.security import get_password_hash, verify_password

register_router = APIRouter(prefix="/register", tags=["Register"])
SECRET_KEY = 'I3ZHkhxYZQ2dSQGNsH3j5K38H'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30
def authenticate_user(username: str, password: str):
    '''
        TODO: get user credentials(e.g email, password) with AWS API from user table
    '''
    pass_str: str
    pass_str ="Test"
    user= { "password": pass_str}
    if user and verify_password(password, user["password"]):
        return user
    return None
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    if data.get("role") == "admin":
        to_encode.update({"isAdmin": True})
    else:
        to_encode.update({"isAdmin": False})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@register_router.post("/")
async def regster_user(user: UserRegister):
    hashed_password = get_password_hash(user.password)

    if user.name == "admin":
        user.role = "admin"

    try:
        '''
            :TODO: Make request to the AWS API to add to the table the user.
        '''
        return {"message": "User registered successfully"}
    except:
        '''
           TODO: Raise exception for email already exist.
        '''

login_router = APIRouter(prefix="/login", tags=["Login"])

@login_router.post("/")
async def login_user(user: UserLogin):
    '''
        TODO: Make request to the AWS API to search for the user, from the email provided
    '''
    db_user = user.email
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Verify the password
    if not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.email},  # Optionally include roles or other claims
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}