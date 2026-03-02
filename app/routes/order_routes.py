from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import make_session, verify_token
from app.models.models import PedidoModel, Status
from app.schemas.schemas import PedidoSchema

order_router = APIRouter(prefix="/pedidos", tags=["orders"], dependencies=[Depends(verify_token)])


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

@order_router.post("/cancelar/{pedido_id}")
async def cancelar_pedido(pedido_id: int, db: Session = Depends(make_session)):
    pedido = db.query(PedidoModel).filter(PedidoModel.id == pedido_id).first()
    if not pedido:
        raise HTTPException(detail= "Pedido nao encontrado", status_code=404)

    pedido.status = Status.CANCELADO
    db.commit()
    return{
        "message": f"Pedido do user {pedido_id} cancelado com sucesso"
    }