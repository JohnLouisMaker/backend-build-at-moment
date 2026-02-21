from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import make_session
from app.models.models import Pedidos
from app.schemas.schemas import pedidosSchema

order_router = APIRouter(prefix="/pedidos", tags=["orders"])


@order_router.get("/")
async def pedidos():
    return {"message": "Get all orders"}


@order_router.post("/pedido")
async def pedido(schema: pedidosSchema, db: Session = Depends(make_session)):
    novo_pedido = Pedidos(usuario=schema.usuario)
    db.add(novo_pedido)
    db.commit()
    db.refresh(novo_pedido)
    return {"message": "Pedido realizado com sucesso!"}
