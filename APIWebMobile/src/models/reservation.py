from pydantic import BaseModel, EmailStr
from src.models.parking import ParkingSpot
from datetime import date, time
from typing import Tuple

class Reservation(BaseModel):
    email: EmailStr
    car_plate: str
    parking_spot: ParkingSpot
    date: date
    hour_range: Tuple[time, time]