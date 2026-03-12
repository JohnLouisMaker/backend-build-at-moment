# 🍕 Orders API — FastAPI + SQLite

API RESTful para gerenciamento de pedidos, construída com **FastAPI**, **SQLAlchemy** e autenticação via **JWT**.

---

## 📋 Sobre o Projeto

Sistema de pedidos com autenticação completa (cadastro, login, refresh de token) e gerenciamento de pedidos com itens. Cada pedido pertence a um usuário e pode conter múltiplos itens (sabor, tamanho, quantidade, preço). Administradores têm acesso irrestrito; usuários comuns gerenciam apenas os próprios pedidos.

---

## 🚀 Tecnologias

| Tecnologia | Uso |
|---|---|
| **FastAPI** | Framework web |
| **SQLAlchemy** | ORM e modelagem do banco |
| **SQLite** | Banco de dados |
| **Alembic** | Migrações do banco |
| **python-jose** | Geração e validação de JWT |
| **passlib[bcrypt]** | Hash de senhas |
| **python-dotenv** | Variáveis de ambiente |

---

## 📁 Estrutura do Projeto

```
├── alembic/                  # Migrações do banco de dados
│   └── versions/
├── app/
│   ├── core/
│   │   └── config.py         # Configurações via .env
│   ├── database/
│   │   └── database.db       # Arquivo SQLite (gerado automaticamente)
│   ├── models/
│   │   └── models.py         # Modelos: UserModel, PedidoModel, ItemPedidoModel
│   ├── routes/
│   │   ├── auth_routes.py    # Rotas de autenticação
│   │   └── order_routes.py   # Rotas de pedidos
│   ├── schemas/
│   │   └── schemas.py        # Schemas Pydantic
│   ├── dependencies.py       # Injeção de dependências e autenticação
│   ├── main.py               # Entry point da aplicação
│   └── security.py           # Contexto bcrypt e OAuth2
├── alembic.ini
├── requirements.txt
└── .env                      # (não versionado)
```

---

## ⚙️ Instalação e Configuração

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd <nome-do-projeto>
```

### 2. Crie e ative o ambiente virtual

```bash
python -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
SECRET_KEY=sua_chave_secreta_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE=30        # em minutos
REFRESH_TOKEN_EXPIRE=7        # em dias
```

### 5. Execute as migrações

```bash
alembic upgrade head
```

### 6. Inicie o servidor

```bash
uvicorn app.main:app --reload
```

A API estará disponível em: `http://127.0.0.1:8000`

Documentação interativa: `http://127.0.0.1:8000/docs`

---

## 🔐 Autenticação

A API usa **JWT** com dois tokens:

- **Access Token** — de curta duração, usado nas requisições autenticadas
- **Refresh Token** — de longa duração, usado para renovar o access token

Todas as rotas protegidas exigem o header:

```
Authorization: Bearer <access_token>
```

---

## 📌 Endpoints

### Auth — `/auth`

| Método | Rota | Descrição | Auth |
|---|---|---|---|
| `POST` | `/auth/signup` | Cadastro de novo usuário | ❌ |
| `POST` | `/auth/login` | Login com email e senha | ❌ |
| `POST` | `/auth/loginform` | Login via OAuth2 form (Swagger) | ❌ |
| `POST` | `/auth/refresh` | Renova o access token | Refresh Token |

**Body — Signup:**
```json
{
  "nome": "João Silva",
  "email": "joao@email.com",
  "senha": "senha123",
  "ativo": true,
  "admin": false
}
```

**Body — Login:**
```json
{
  "email": "joao@email.com",
  "senha": "senha123"
}
```

---

### Pedidos — `/pedidos`

| Método | Rota | Descrição | Permissão |
|---|---|---|---|
| `GET` | `/pedidos/` | Lista todos os pedidos | Admin |
| `GET` | `/pedidos/pedido/{pedido_id}` | Visualiza um pedido | Dono ou Admin |
| `GET` | `/pedidos/listar/{usuario_id}` | Lista pedidos de um usuário | Dono ou Admin |
| `POST` | `/pedidos/criar_pedido` | Cria um novo pedido | Autenticado |
| `POST` | `/pedidos/adicionar_item/{pedido_id}` | Adiciona item ao pedido | Dono ou Admin |
| `POST` | `/pedidos/finalizar/{pedido_id}` | Finaliza o pedido | Dono ou Admin |
| `POST` | `/pedidos/cancelar/{pedido_id}` | Cancela o pedido | Dono ou Admin |
| `DELETE` | `/pedidos/remover_item/{pedido_id}/{item_id}` | Remove um item do pedido | Dono ou Admin |

**Body — Adicionar item:**
```json
{
  "quantidade": 2,
  "sabor": "Calabresa",
  "tamanho": "Grande",
  "preco_unitario": 45.90
}
```

---

## 🗄️ Modelos do Banco

### `usuario`
| Campo | Tipo | Descrição |
|---|---|---|
| `id` | Integer PK | Identificador único |
| `nome` | String(100) | Nome do usuário |
| `email` | String(150) unique | Email de login |
| `senha` | String(250) | Senha hasheada com bcrypt |
| `ativo` | Boolean | Conta ativa/inativa |
| `admin` | Boolean | Permissão de administrador |

### `pedidos`
| Campo | Tipo | Descrição |
|---|---|---|
| `id` | Integer PK | Identificador único |
| `usuario_id` | FK → usuario | Dono do pedido |
| `status` | Enum | `PENDENTE`, `FINALIZADO`, `CANCELADO` |
| `preco` | Float | Valor total calculado automaticamente |

### `itens_pedidos`
| Campo | Tipo | Descrição |
|---|---|---|
| `id` | Integer PK | Identificador único |
| `pedido_id` | FK → pedidos | Pedido ao qual pertence |
| `sabor` | String(100) | Sabor do item |
| `tamanho` | String(100) | Tamanho do item |
| `quantidade` | Integer | Quantidade |
| `preco_unitario` | Float | Preço por unidade |

---

## 🔄 Migrações com Alembic

```bash
# Criar nova migration
alembic revision --autogenerate -m "descricao_da_migration"

# Aplicar migrations pendentes
alembic upgrade head

# Reverter última migration
alembic downgrade -1

# Ver histórico
alembic history
```

---

## 📄 Licença

Este projeto está sob a licença MIT.
