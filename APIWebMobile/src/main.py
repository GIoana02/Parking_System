from fastapi import FastAPI
from src.routers.register_router import register_router, login_router
from src.routers.plate_router import plate_router
from src.routers.reservation_router import reservation_router

app = FastAPI()

app.include_router(register_router)
app.include_router(login_router)
app.include_router(reservation_router)
app.include_router(plate_router)
