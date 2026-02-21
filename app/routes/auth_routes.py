from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import make_session
from app.models.models import UsersModel
from app.schemas.schemas import usersSchema
from app.security import bcrypt_context

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.get("/")
async def home():
    return {"message": "Auth"}


@auth_router.post("/signup", status_code=201)
async def signup(schema: usersSchema, db: Session = Depends(make_session)):
    usuario_existe = (
        db.query(UsersModel).filter(UsersModel.email == schema.email).first()
    )
    if usuario_existe:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    else:
        senha_hash = bcrypt_context.hash(schema.senha)
        novo_usuario = UsersModel(
            nome=schema.nome, email=schema.email, senha=senha_hash
        )
        db.add(novo_usuario)
        db.commit()
        db.refresh(novo_usuario)
        return {"message": f"Cadastro realizado com sucesso! Bem-vindo {schema.nome}"}
