from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import ALGORITHM, SECRET_KEY
from app.models.models import UserModel, db
from app.security import oauth2_schema


def make_session():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()


# REFRESH
def verify_token(token: str = Depends(oauth2_schema)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado.")


# VALIDAÇÃO DO USER E TOKEN ACCESS
def get_current_user(
    payload: dict = Depends(verify_token), session: Session = Depends(make_session)
):
    if payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="Token de acesso exigido.")

    user = session.query(UserModel).filter(UserModel.id == payload.get("sub")).first()
    if not user:
        raise HTTPException(status_code=401, detail="Usuário não encontrado.")
    return user
