from datetime import timedelta, datetime
from http.client import HTTPException
from src.dynamoDB_interaction import get_table, hash_password
import jwt as jwt
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from boto3.dynamodb.conditions import Key
from src.models.user import UserRegistration, UserLogin
from src.security import get_password_hash, verify_password


register_router = APIRouter(prefix="/register", tags=["Register"])
login_router = APIRouter(prefix="/login", tags=["Login"])
SECRET_KEY = 'I3ZHkhxYZQ2dSQGNsH3j5K38H'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

@register_router.post("/")
async def register_user(user_data: UserRegistration):
    table = get_table("User")
    user_id = hash_password(user_data.email)  # Use the email to generate a hashed user ID
    encrypted_password = hash_password(user_data.password)  # Encrypt the password
    try:
        response = table.put_item(
            Item={
                "user_id": user_id,
                "name": user_data.name,
                "email": user_data.email,
                "phone": user_data.phone,
                "car_plate_ids": user_data.car_plate_ids,
                "role": user_data.role,
                "password_hash": encrypted_password
            },
            ConditionExpression="attribute_not_exists(user_id)"  # Ensure the user does not already exist
        )
        return {"user_id": user_id, "email": user_data.email, "message": "User registered successfully"}
    except Exception as e:
        raise HTTPException(400, str(e))  # Corrected the exception handling here

@login_router.post("/")
async def login_user(email: str, password: str):
    table = get_table("User")
    user_id = hash_password(email)
    encrypted_password = hash_password(password)
    response = table.get_item(
        Key={"user_id": user_id}
    )
    user = response.get("Item")
    if user and user['password_hash'] == encrypted_password:
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=400, detail="Invalid login credentials")

