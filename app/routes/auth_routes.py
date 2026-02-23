from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import make_session
from app.models.models import UserModel
from app.schemas.schemas import UserSchema
# from app.schemas.schemas import LoginSchema
from app.security import bcrypt_context

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.get("/")
async def home():
    return {"message": "Auth"}


@auth_router.post("/signup", status_code=201)
async def signup(schema: UserSchema, db: Session = Depends(make_session)):
    user_exists = db.query(UserModel).filter(UserModel.email == schema.email).first()
    if user_exists:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    else:
        password_hash = bcrypt_context.hash(schema.senha)
        new_user = UserModel(
            nome=schema.nome, email=schema.email, senha=password_hash
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {
            "message": f"Cadastro realizado com sucesso! Bem-vindo {schema.nome}"
        }


# @auth_router.post("/login")
# async def login(schema: LoginSchema, db: Session = Depends(make_session)):
#     user = 