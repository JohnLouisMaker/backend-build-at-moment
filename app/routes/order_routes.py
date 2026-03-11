from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app.dependencies import get_current_user, make_session
from app.models.models import ItemPedidoModel, PedidoModel, Status, UserModel
from app.schemas.schemas import ItemPedidoSchema

order_router = APIRouter(prefix="/pedidos", tags=["orders"])



def verificar_permissao_pedido(pedido, current_user):
    if current_user.admin:
        return True
    if pedido.usuario_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Acesso negado: você não tem permissão para acessar este pedido.",
        )
    return True

#------------------------------------------------------------------------------
# --- ROTAS ---

@order_router.get("/")
async def listar_pedidos(
    db: Session = Depends(make_session),
    current_user: UserModel = Depends(get_current_user),
):
    if not current_user.admin:
        raise HTTPException(
            status_code=403, detail="Acesso negado: apenas administradores."
        )

    pedidos = db.query(PedidoModel).options(joinedload(PedidoModel.itens)).all()
    return {"pedidos": pedidos}

@order_router.get("/pedido/{pedido_id}")
async def visualizar_pedido(
    pedido_id: int,
    db: Session = Depends(make_session),
    current_user: UserModel = Depends(get_current_user),
):
  
    pedido = db.query(PedidoModel).options(joinedload(PedidoModel.itens)).filter(PedidoModel.id == pedido_id).first()
    
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    verificar_permissao_pedido(pedido, current_user)

    return {"pedido": pedido}

@order_router.get("/listar/{usuario_id}")
async def listar_pedidos_usuario(
    usuario_id: int,
    db: Session = Depends(make_session),
    current_user: UserModel = Depends(get_current_user),
):

    if not current_user.admin and current_user.id != usuario_id:
        raise HTTPException(
            status_code=403, detail="Acesso negado: você não tem permissão."
        )

    pedidos = db.query(PedidoModel).options(joinedload(PedidoModel.itens)).filter(PedidoModel.usuario_id == usuario_id).all()
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

    verificar_permissao_pedido(pedido, current_user)

    if pedido.status == Status.CANCELADO:
        return {"message": "Este pedido já está cancelado!"}

    pedido.status = Status.CANCELADO
    db.commit()
    return {"message": f"Pedido {pedido_id} cancelado com sucesso"}

@order_router.post("/finalizar/{pedido_id}")
async def finalizar_pedido(
    pedido_id: int,
    db: Session = Depends(make_session),
    current_user: UserModel = Depends(get_current_user),
):
    pedido = db.query(PedidoModel).filter(PedidoModel.id == pedido_id).first()

    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    verificar_permissao_pedido(pedido, current_user)

    if pedido.status == Status.FINALIZADO:
        return {"message": "Este pedido já está finalizado!"}

    pedido.status = Status.FINALIZADO
    db.commit()
    return {"message": f"Pedido {pedido_id} finalizado com sucesso"}

@order_router.post("/adicionar_item/{pedido_id}")
async def adicionar_item(
    pedido_id: int,
    schema: ItemPedidoSchema,
    db: Session = Depends(make_session),
    current_user: UserModel = Depends(get_current_user),
):
    pedido = db.query(PedidoModel).filter(PedidoModel.id == pedido_id).first()

    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    verificar_permissao_pedido(pedido, current_user)

    if pedido.status == Status.CANCELADO or pedido.status == Status.FINALIZADO:
        raise HTTPException(status_code=400, detail=f"Esse pedido está {pedido.status}!")

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

@order_router.delete("/remover_item/{pedido_id}/{item_id}")
async def remover_item(
    pedido_id: int,
    item_id: int,
    db: Session = Depends(make_session),
    current_user: UserModel = Depends(get_current_user),
):
    pedido = db.query(PedidoModel).filter(PedidoModel.id == pedido_id).first()
    
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    verificar_permissao_pedido(pedido, current_user)

    if pedido.status == Status.CANCELADO or pedido.status == Status.FINALIZADO:
        return {"message": f"Este pedido já está {pedido.status} e não pode ser alterado!"}

    item = (
        db.query(ItemPedidoModel)
        .filter(ItemPedidoModel.id == item_id, ItemPedidoModel.pedido_id == pedido_id)
        .first()
    )
    
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado neste pedido")

    pedido.subtrair_item_do_total(item.quantidade, item.preco_unitario)
    db.delete(item)
    db.add(pedido)
    db.commit()
    db.refresh(pedido)

    return {
        "message": "Item removido com sucesso",
        "total_pedido_updated": pedido.preco,
    }