from typing import Optional

from pydantic import BaseModel


class UserSchema(BaseModel):
    nome: str
    email: str
    senha: str
    ativo: Optional[bool]
    admin: Optional[bool]

    class Config:
        from_attributes = True


class LoginSchema(BaseModel):
    email: str
    senha: str

    class Config:
        from_attributes = True


class PedidoSchema(BaseModel):
    usuario_id: int

    class Config:
        from_attributes = True
