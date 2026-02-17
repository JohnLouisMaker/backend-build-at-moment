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
from sqlalchemy.orm import declarative_base

# Conexão Do Meu Banco
db = create_engine("sqlite:///database/database.db")

# Base Do Meu Banco
base = declarative_base()


# Criando Classe/Tabela
# TABELA USUARIOS
class Users(base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    nome = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    senha = Column(String(250), nullable=False)
    ativo = Column(Boolean, nullable=False, default=True)
    admin = Column(Boolean, nullable=False, default=False)

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


class Pedidos(base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    usuario = Column("usuario", Integer, ForeignKey("usuario.id"), nullable=False)
    status = Column("status", Enum(Status), nullable=False, default=Status.PENDENTE)
    preco = Column("preco", Float, nullable=False)

    def __init__(self, usuario, status=Status.PENDENTE, preco=0):
        self.status = status
        self.usuario = usuario
        self.preco = preco


# TABELA ITENS DE PEDIDOS
class ItensPedidos(base):
    __tablename__ = "itens_pedidos"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    quantidade = Column(Integer, nullable=False)
    sabor = Column(String(100), nullable=False)
    tamanho = Column(String(100), nullable=False)
    preco_unitario = Column(Float, nullable=False)
    pedido = Column(Integer, ForeignKey("pedidos.id"), nullable=False)

    def __init__(self, quantidade, sabor, tamanho, preco_unitario, pedido):
        self.quantidade = quantidade
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario
        self.pedido = pedido
