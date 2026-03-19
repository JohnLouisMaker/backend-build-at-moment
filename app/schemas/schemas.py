from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


# --- USUÁRIO ---
class UserSchema(BaseModel):
    nome: str
    email: str
    senha: str
    ativo: Optional[bool] = True
    admin: Optional[bool] = False


# --- LOGIN ---
class LoginSchema(BaseModel):
    email: str
    senha: str


# --- ITENS DE PEDIDO ---
class ItemPedidoSchema(BaseModel):
    quantidade: int
    sabor: str
    tamanho: str
    preco_unitario: float


class ItemPedidoSchemaResponse(BaseModel):
    id: int
    quantidade: int
    sabor: str
    tamanho: str
    preco_unitario: float

    model_config = ConfigDict(from_attributes=True)


# --- PEDIDO ---
class StatusSchema(str, Enum):
    FINALIZADO = "FINALIZADO"
    PENDENTE = "PENDENTE"
    CANCELADO = "CANCELADO"


class PedidoSchemaResponse(BaseModel):
    id: int
    usuario_id: int
    status: StatusSchema
    preco: float
    itens: List[ItemPedidoSchemaResponse] = []

    model_config = ConfigDict(from_attributes=True)
