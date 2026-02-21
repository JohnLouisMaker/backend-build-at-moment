from typing import Optional

from pydantic import BaseModel


class usersSchema(BaseModel):
    nome: str
    email: str
    senha: str
    ativo: Optional[bool]
    admin: Optional[bool]

    class Config:
        from_attributes = True


class pedidosSchema(BaseModel):
    usuario: int

    class Config:
        from_attributes = True
