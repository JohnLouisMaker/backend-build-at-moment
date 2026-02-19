from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dependencies import make_session
from models.models import Users as UserModel
from schemas.schemas import Users as UserSchema
from security import bcrypt_context

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.get("/")
async def home():
    return {"message": "Auth"}


@auth_router.post("/signup")
async def signup(schema: UserSchema, db: Session = Depends(make_session)):
    usuario_existe = db.query(UserModel).filter(UserModel.email == schema.email).first()
    if usuario_existe:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    else:
        senha_hash = bcrypt_context.hash(schema.senha)
        novo_usuario = UserModel(nome=schema.nome, email=schema.email, senha=senha_hash)
        db.add(novo_usuario)
        db.commit()
        return {"message": f"Cadastro realizado com sucesso! Bem-vindo {schema.nome}"}
