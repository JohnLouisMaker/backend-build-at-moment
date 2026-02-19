import os

from dotenv import load_dotenv
from fastapi import FastAPI

from routes.auth_routes import auth_router
from routes.order_routes import order_router

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
app = FastAPI()

# Incluindo Rotas
app.include_router(auth_router)
app.include_router(order_router)


# Rota Raiz
@app.get("/")
async def root():
    return {"message": "API Python com FastAPI!"}
