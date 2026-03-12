from typing import Optional, List
from pydantic import BaseModel

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

    class Config:
        from_attributes = True


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

    class Config:
        from_attributes = True


# --- PEDIDO ---
class PedidoSchema(BaseModel):
    usuario_id: int

class PedidoSchemaResponse(BaseModel):

    id: int
    usuario_id: int 
    status: str
    preco: float
    itens: List[ItemPedidoSchemaResponse] = [] 

    class Config:
        from_attributes = True