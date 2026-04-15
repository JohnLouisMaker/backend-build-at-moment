import os
import shutil
from uuid import uuid4

from app.dependencies import get_current_user, make_session
from app.models.models import CategoriaEnum, ItemCardapio, UserModel
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

product_router = APIRouter(prefix="/cardapio", tags=["cardapio"])

UPLOAD_DIR = "static/uploads"


# ROTA PRIVADA: Só
@product_router.post("/adicionar")
async def adicionar_item_cardapio(
    nome: str = Form(...),
    descricao: str = Form(None),
    preco: float = Form(...),
    categoria: CategoriaEnum = Form(...),
    imagem: UploadFile = File(...),
    db: Session = Depends(make_session),
    current_user: UserModel = Depends(get_current_user),
):
    if not current_user.admin:
        raise HTTPException(
            status_code=403, detail="Apenas administradores podem gerenciar o cardápio."
        )

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Gerar nome único para a foto
    ext = os.path.splitext(imagem.filename)[1]
    filename = f"{uuid4()}{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(imagem.file, buffer)

    novo_item = ItemCardapio(
        nome=nome,
        descricao=descricao,
        preco=preco,
        categoria=categoria,
        imagem_url=f"/static/uploads/{filename}",
    )

    db.add(novo_item)
    db.commit()
    db.refresh(novo_item)
    return {"message": "Item adicionado ao cardápio!", "item": novo_item}

@product_router.patch("/editar/{item_id}")
async def editar_preco(
    item_id: int, 
    novo_preco: float, 
    db: Session = Depends(make_session),
    current_user: UserModel = Depends(get_current_user)
):
    if not current_user.admin:
        raise HTTPException(status_code=403, detail="Acesso negado")

    item = db.query(ItemCardapio).filter(ItemCardapio.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")

    item.preco = novo_preco
    db.commit()
    return {"message": "Preço atualizado!", "item": item.nome, "novo_preco": item.preco}
