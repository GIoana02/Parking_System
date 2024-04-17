from typing import List
from src.models.car import CarPlate
from pydantic import BaseModel, Field, EmailStr


class UserRegister(BaseModel):
    name: str
    email: EmailStr
    phone_number: str
    password: str
    car_plates_id: List[CarPlate]
    role: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    role: str