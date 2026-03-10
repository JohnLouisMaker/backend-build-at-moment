import enum

from sqlalchemy import (
    Boolean,
    Column,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    create_engine,
)
from sqlalchemy.orm import declarative_base, relationship

# Conexão Do Meu Banco
db = create_engine("sqlite:///./app/database/database.db")
Base = declarative_base()


# TABELA USUARIOS
class UserModel(Base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    nome = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    senha = Column(String(250), nullable=False)
    ativo = Column(Boolean, nullable=False, default=True)
    admin = Column(Boolean, nullable=False, default=False)

    # NOME MELHOR: "pedidos" (Plural, pois um usuário tem vários)
    pedidos = relationship("PedidoModel", back_populates="usuario")

    def __init__(self, nome, email, senha, ativo=True, admin=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin


# TABELA PEDIDOS
class Status(enum.Enum):
    FINALIZADO = "Finalizado"
    PENDENTE = "Pendente"
    CANCELADO = "Cancelado"


class PedidoModel(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    usuario_id = Column( Integer, ForeignKey("usuario.id"), nullable=False)
    status = Column(Enum(Status), nullable=False, default=Status.PENDENTE)
    preco = Column(Float, default=0.0, nullable=False)

    usuario = relationship("UserModel", back_populates="pedidos")
    itens = relationship("ItemPedidoModel", cascade="all, delete-orphan", back_populates="pedido")

    def __init__(self, usuario_id, status=Status.PENDENTE, preco=0):
        self.status = status
        self.usuario_id = usuario_id
        self.preco = preco

    def adicionar_item_ao_total(self, quantidade, preco_unitario):
        valor_novo_item = quantidade * preco_unitario
        self.preco = (self.preco or 0.0) + valor_novo_item
        return self.preco
    
    def subtrair_item_do_total(self, quantidade, preco_unitario):
        valor_removido = quantidade * preco_unitario
        novo_preco = (self.preco or 0.0) - valor_removido
        
        self.preco = max(0.0, novo_preco)
        return self.preco


# TABELA ITENS DE PEDIDOS
class ItemPedidoModel(Base):
    __tablename__ = "itens_pedidos"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    quantidade = Column(Integer, nullable=False)
    sabor = Column(String(100), nullable=False)
    tamanho = Column(String(100), nullable=False)
    preco_unitario = Column(Float, nullable=False)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)

    
    pedido = relationship("PedidoModel", back_populates="itens")

    def __init__(self, quantidade, sabor, tamanho, preco_unitario, pedido_id):
        self.quantidade = quantidade
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario
        self.pedido_id = pedido_id

  