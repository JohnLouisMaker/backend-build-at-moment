from fastapi import APIRouter

order_router = APIRouter(prefix="/pedidos", tags=["orders"])


@order_router.get("/")
async def pedidos():
    return {"message": "Get all orders"}
