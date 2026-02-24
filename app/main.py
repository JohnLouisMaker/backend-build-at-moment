from fastapi import FastAPI

from app.routes.auth_routes import auth_router
from app.routes.order_routes import order_router

app = FastAPI()

# Incluindo Rotas
app.include_router(auth_router)
app.include_router(order_router)


# Rota Raiz
@app.get("/")
async def root():
    return {"message": "API Python com FastAPI!"}
