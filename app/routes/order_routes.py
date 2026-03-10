from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_current_user, make_session
from app.models.models import ItemPedidoModel, PedidoModel, Status, UserModel
from app.schemas.schemas import ItemPedidoSchema

order_router = APIRouter(prefix="/pedidos", tags=["orders"])


@order_router.get("/")
async def listar_pedidos(
    db: Session = Depends(make_session),
    current_user: UserModel = Depends(get_current_user),
):

    if not current_user.admin:
        raise HTTPException(
            status_code=403, detail="Acesso negado: apenas administradores."
        )

    pedidos = db.query(PedidoModel).all()
    return {"pedidos": pedidos}


@order_router.post("/criar_pedido")
async def criar_pedido(
    db: Session = Depends(make_session),
    current_user: UserModel = Depends(get_current_user),
):

    novo_pedido = PedidoModel(usuario_id=current_user.id)
    db.add(novo_pedido)
    db.commit()
    db.refresh(novo_pedido)
    return {"message": "Pedido realizado com sucesso!", "id": novo_pedido.id}


@order_router.post("/cancelar/{pedido_id}")
async def cancelar_pedido(
    pedido_id: int,
    db: Session = Depends(make_session),
    current_user: UserModel = Depends(get_current_user),
):
    pedido = db.query(PedidoModel).filter(PedidoModel.id == pedido_id).first()

    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    is_owner = pedido.usuario_id == current_user.id
    if not current_user.admin and not is_owner:
        raise HTTPException(
            status_code=403, detail="Sem permissão para cancelar este pedido"
        )

    if pedido.status == Status.CANCELADO:
        return {"message": "Este pedido já está cancelado!"}

    pedido.status = Status.CANCELADO
    db.commit()
    return {"message": f"Pedido {pedido_id} cancelado com sucesso"}


@order_router.post("/adicionar_item/{pedido_id}")
async def adicionar_item(
    pedido_id: int,
    schema: ItemPedidoSchema,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(make_session),
):
    pedido = db.query(PedidoModel).filter(PedidoModel.id == pedido_id).first()

    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    if pedido.status == Status.CANCELADO:
        raise HTTPException(status_code=400, detail="Esse pedido está cancelado!")

    is_owner = pedido.usuario_id == current_user.id
    if not current_user.admin and not is_owner:
        raise HTTPException(
            status_code=403,
            detail="Acesso negado: você não tem permissão para realizar esta ação.",
        )

    new_item = ItemPedidoModel(
        pedido_id=pedido_id,
        quantidade=schema.quantidade,
        sabor=schema.sabor,
        tamanho=schema.tamanho,
        preco_unitario=schema.preco_unitario,
    )

    pedido.adicionar_item_ao_total(new_item.quantidade, new_item.preco_unitario)
    db.add(new_item)
    db.add(pedido)
    db.commit()
    db.refresh(new_item)
    db.refresh(pedido)
    return {
        "message": "Item adicionado com sucesso",
        "item": new_item,
        "total_pedido": pedido.preco,
    }