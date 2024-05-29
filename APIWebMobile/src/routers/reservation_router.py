import boto3
from boto3.dynamodb.conditions import Key
from fastapi import APIRouter, Path, HTTPException
from src.dynamoDB_interaction import get_table, hash_password
from typing import List, Dict


reservation_router = APIRouter(prefix="/reservation", tags=["Reservation"])

@reservation_router.post("/create-reservation/", response_model=Dict[str, str])
async def create_reservation(license_plate: str, spot_id: str, user_id: str, date: str, hour: str, status: str = "confirmed"):
    table = get_table("Reservations")  # Make sure this is the correct table name
    reservation_id = hash_password(user_id + date + hour)  # Simple reservation ID generator
    try:
        response = table.put_item(
            Item={
                'license_plate': license_plate,
                'spot_id': spot_id,
                'user_id': user_id,
                'reservation_id': hash_password(user_id + date + hour),
                'date': date,
                'hour': hour,
                'status': status
            }
        )
        return {"reservation_id": reservation_id, "status": "Reservation confirmed"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
@reservation_router.put("/update_reservation/")
async def update_reservation(reservation_id: str, status: str):
    table = get_table("Reservations")
    response = table.update_item(
        Key={"reservation_id": reservation_id},
        UpdateExpression="set #st = :s",
        ExpressionAttributeValues={
            ":s": status
        },
        ExpressionAttributeNames={
            "#st": "status"
        },
        ReturnValues="UPDATED_NEW"
    )
    return {"message": "Reservation updated", "new_status": status}

@reservation_router.get("/user/{user_id}/car-plates", response_model=List[str])
async def get_car_plates(name: str):
    table = get_table("User")
    try:
        response = table.scan(
            FilterExpression=Key('name').eq(name)
        )
        if 'Items' in response and response['Items']:
            car_plates = response['Items'][0].get('car_plate_ids', [])
            return car_plates
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


