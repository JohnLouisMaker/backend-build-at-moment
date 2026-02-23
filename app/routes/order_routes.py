from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import make_session
from app.models.models import PedidoModel
from app.schemas.schemas import PedidoSchema

order_router = APIRouter(prefix="/pedidos", tags=["orders"])


@order_router.get("/")
async def listar_pedidos():
    return {"message": "Get all orders"}


@order_router.post("/")
async def criar_pedido(schema: PedidoSchema, db: Session = Depends(make_session)):
    novo_pedido = PedidoModel(usuario_id=schema.usuario_id)
    db.add(novo_pedido)
    db.commit()
    db.refresh(novo_pedido)
    return {
        "message": f"Pedido realizado com sucesso! ID do pedido: {novo_pedido.id}"
    }