from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import ALGORITHM, SECRET_KEY
from app.models.models import UserModel, db


def make_session():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()


def verify_token(token, session: Session = Depends(make_session)):
    try:
        payload_info = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload_info["sub"]
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado.")

    user = session.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Usuário não autorizado.")

    return user
