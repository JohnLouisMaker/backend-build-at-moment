from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from sqlalchemy.orm import Session

from app.core.config import (
    ACCESS_TOKEN_EXPIRE,
    ALGORITHM,
    REFRESH_TOKEN_EXPIRE,
    SECRET_KEY,
)
from app.dependencies import make_session, verify_token
from app.models.models import UserModel
from app.schemas.schemas import LoginSchema, UserSchema
from app.security import bcrypt_context

auth_router = APIRouter(prefix="/auth", tags=["auth"])


def authenticate(email: str, senha: str, session: Session) -> UserModel | None:
    user = session.query(UserModel).filter(UserModel.email == email).first()
    if user and bcrypt_context.verify(senha, user.senha):
        return user
    return None


def create_token(id: int, token_type: str, duration: timedelta):
    now = datetime.now(timezone.utc)
    payload_info = {
        "sub": str(id),
        "type": token_type,
        "iat": now,
        "exp": now + duration,
    }
    jwt_token = jwt.encode(payload_info, SECRET_KEY, algorithm=ALGORITHM)
    return jwt_token

def generate_auth_tokens(user_id: int):
    access_token = create_token(
        user_id,
        token_type="access",
        duration=timedelta(minutes=ACCESS_TOKEN_EXPIRE),
    )
    refresh_token = create_token(
        user_id,
        token_type="refresh",
        duration=timedelta(days=REFRESH_TOKEN_EXPIRE),
    )
    return access_token, refresh_token

# ----------------------------------------
# ----------------------------------------
# ROTAS

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
            nome=schema.nome,
            email=schema.email,
            senha=password_hash,
            ativo=schema.ativo,
            admin=schema.admin,
        )

        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        access_token, refresh_token = generate_auth_tokens(new_user.id)
        return {
            "message": f"Cadastro realizado com sucesso! Bem-vindo {new_user.nome}",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer",
        }


@auth_router.post("/login")
async def login(schema: LoginSchema, db: Session = Depends(make_session)):
    user = authenticate(schema.email, schema.senha, db)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    
    access_token, refresh_token = generate_auth_tokens(user.id)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer",
    }


@auth_router.post("/loginform")
async def loginform(
    schema: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(make_session)
):
    user = authenticate(schema.username, schema.password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    
    access_token, refresh_token = generate_auth_tokens(user.id)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer",
    }


@auth_router.post("/refresh")
async def refresh_token(
    data: dict = Depends(verify_token), db: Session = Depends(make_session)
):

    token_type = data.get("type")
    user_id = data.get("sub")

    if token_type != "refresh":
        raise HTTPException(status_code=401, detail="Refresh token necessário")

    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Usuário inexistente")

    access_token, _ = generate_auth_tokens(user.id)

    return {
        "access_token": access_token,
        "token_type": "Bearer",
    }
