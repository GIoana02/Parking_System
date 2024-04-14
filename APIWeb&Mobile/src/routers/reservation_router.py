from fastapi import APIRouter

reservation_router = APIRouter(prefix="/reservation", tags=["Reservation"])


@reservation_router.post("/{user}")
async def reservation():
    '''
        TO MAKE the reservation we need the account credentials(the user must be logged in), the car_id, the parking spot
        & also the date & time the reservation is made

        TODO: implement function to take from the AWS API the car plates specific to the user in the token session details
        TODO: implement function to add reservation in table of reservation with AWS API
    '''