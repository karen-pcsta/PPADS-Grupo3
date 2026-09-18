# Orders Management API

Um backend RESTful para um sistema simplificado de gerenciamento de pedidos de e-commerce, construído com **FastAPI**, **SQLAlchemy** e **PostgreSQL**. Ele cobre o fluxo principal de compras — autenticação, catálogo de produtos, gerenciamento de carrinho e criação de pedidos — com controle de acesso baseado em papéis (roles).

---

## Sumário

- [Funcionalidades](#funcionalidades)
- [Stack](#stack)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Modelos de Dados](#modelos-de-dados)
- [Referência da API](#referência-da-api)
- [Primeiros Passos](#primeiros-passos)
- [Variáveis de Ambiente](#variáveis-de-ambiente)
- [Migrações do Banco de Dados](#migrações-do-banco-de-dados)
- [Populando o Banco de Dados](#populando-o-banco-de-dados)

---

## Funcionalidades

- **Autenticação JWT** — cadastro, login, logout e endpoint do usuário atual
- **Controle de acesso baseado em papéis** — papéis `customer` (cliente) e `admin` aplicados através de dependências do FastAPI
- **Catálogo de produtos** — listagem e detalhe de produtos (gestão administrativa do catálogo fica para uma próxima entrega)
- **Gerenciamento de carrinho** — carrinho por usuário, com operações de adicionar, atualizar e remover itens
- **Ciclo de vida do pedido** — criação de pedido a partir do carrinho, listagem e visualização (conclusão e cancelamento ficam para uma próxima entrega)
- **Tratamento de erros estruturado** — hierarquia de exceções customizada mapeada para códigos de status HTTP
- **Migrações com Alembic** — gerenciamento versionado de schema
- **Script de seed** — popula o catálogo de produtos a partir de um arquivo JSON

---

## Stack

| Camada | Tecnologia |
|---|---|
| Framework web | FastAPI 0.135 |
| Servidor ASGI | Uvicorn 0.42 |
| ORM | SQLAlchemy 2.0 |
| Banco de dados | PostgreSQL (psycopg2-binary) |
| Migrações | Alembic 1.18 |
| Autenticação | python-jose (JWT) + passlib / bcrypt |
| Validação | Pydantic v2 + pydantic-settings |
| Executor de tarefas | taskipy |

---

## Estrutura do Projeto

```
orders_management/
├── app/
│   ├── core/
│   │   ├── dependencies.py    # Injetores de dependência do FastAPI (get_db, verify_jwt, verify_admin)
│   │   ├── exceptions.py      # Hierarquia de exceções customizada
│   │   ├── security.py        # Hash de senha e criação de JWT
│   │   └── settings.py        # Configuração via pydantic-settings (lê o .env)
│   ├── database/
│   │   ├── base.py            # Base declarativa do SQLAlchemy
│   │   └── session.py         # Engine e fábrica de SessionLocal
│   ├── models/
│   │   └── models.py          # Modelos ORM: User, Product, Cart, CartItem, Order, OrderItem
│   ├── repositories/          # Camada de acesso a dados (um arquivo por modelo)
│   ├── routers/               # Rotas do FastAPI: auth, products, cart, orders
│   ├── schemas/                # Schemas Pydantic de request/response
│   ├── services/               # Camada de regras de negócio
│   └── main.py                 # Fábrica da aplicação, middlewares, registro de rotas
├── migrations/                 # Ambiente e versões de migração do Alembic
├── scripts/
│   ├── products.json           # Dados de produtos de exemplo
│   └── seed_products.py        # Script de seed do banco de dados
├── alembic.ini
├── pyproject.toml
└── .env                        # (não versionado) veja Variáveis de Ambiente
```

---

## Modelos de Dados

```
User ──── Cart ──── CartItem ──── Product
  │                                  │
  └────── Order ──── OrderItem ──────┘
```

| Modelo | Campos principais |
|---|---|
| `User` | `public_id` (UUID), `username`, `email`, `password` (com hash), `role` |
| `Product` | `public_id` (UUID), `name`, `description`, `price` |
| `Cart` | relação um-para-um com `User` |
| `CartItem` | `cart_id`, `product_id`, `quantity`, `unit_price` |
| `Order` | `public_id` (UUID), `status` (`pending` → `completed` / `cancelled_*`), `total`, `created_at` |
| `OrderItem` | `order_id`, `product_id`, `quantity`, `unit_price` |

---

## Referência da API

Todos os endpoints (exceto cadastro/login) exigem um token `Bearer` no cabeçalho `Authorization`.

### Autenticação — `/auth`

| Método | Rota | Acesso | Descrição |
|---|---|---|---|
| `POST` | `/auth/register` | Público | Cria uma nova conta de cliente |
| `POST` | `/auth/login` | Público | Autentica e retorna um JWT |
| `POST` | `/auth/logout` | Autenticado | Invalida a sessão (do lado do cliente) |
| `GET` | `/auth/me` | Autenticado | Retorna o perfil do usuário atual |

### Produtos — `/products`

| Método | Rota | Acesso | Descrição |
|---|---|---|---|
| `GET` | `/products/` | Autenticado | Lista todos os produtos |
| `GET` | `/products/{public_id}` | Autenticado | Obtém um único produto |

> Nesta entrega o catálogo é somente leitura — criação/edição/remoção de produtos (admin) ficam para uma próxima entrega. Por isso o [seed script](#populando-o-banco-de-dados) é a única forma de popular produtos por enquanto.

### Carrinho — `/cart`

| Método | Rota | Acesso | Descrição |
|---|---|---|---|
| `GET` | `/cart/` | Autenticado | Obtém o carrinho do usuário atual |
| `POST` | `/cart/items` | Autenticado | Adiciona um item ao carrinho |
| `PUT` | `/cart/items/{public_id}` | Autenticado | Atualiza a quantidade de um item |
| `DELETE` | `/cart/items/{public_id}` | Autenticado | Remove um item do carrinho |

### Pedidos — `/orders`

| Método | Rota | Acesso | Descrição |
|---|---|---|---|
| `POST` | `/orders/` | Autenticado | Cria um pedido a partir do carrinho atual |
| `GET` | `/orders/` | Autenticado | Lista pedidos (próprios pedidos; todos os pedidos para admins) |
| `GET` | `/orders/{public_id}` | Autenticado | Obtém um pedido específico |

> Nesta entrega não há como concluir (admin) ou cancelar um pedido depois de criado — essas ações ficam para uma próxima entrega.

A documentação interativa fica disponível em `http://localhost:8000/docs` assim que o servidor estiver rodando.

---

## Primeiros Passos

### Pré-requisitos

- **Python ≥ 3.12**
  - **Windows:** baixe o instalador em [python.org/downloads](https://www.python.org/downloads/) (marque "Add python.exe to PATH" durante a instalação).
  - **Ubuntu/Debian:** a versão padrão do sistema costuma ser mais antiga (ex.: Ubuntu 22.04 vem com 3.10). Instale a 3.12 via [deadsnakes PPA](https://launchpad.net/~deadsnakes/+archive/ubuntu/ppa):
    ```bash
    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt update
    sudo apt install python3.12 python3.12-venv
    ```
  - **macOS:** `brew install python@3.12`
- PostgreSQL rodando localmente
- [Poetry](https://python-poetry.org/) ≥ 2.0 instalado
  - Este projeto usa o formato de `pyproject.toml` do Poetry 2.x (seção `[project]`). Se o Poetry já estiver instalado no seu sistema, confira a versão com `poetry --version` antes de continuar.
  - **Windows/macOS/Linux:** instale (ou atualize) com o instalador oficial, que sempre traz a versão mais recente:
    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```
    No Windows, rode o equivalente em PowerShell:
    ```powershell
    (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
    ```
  - Evite instalar o Poetry via `apt` — os repositórios do Ubuntu costumam ficar presos em versões antigas (ex.: 1.1.x), incompatíveis com este projeto.

### 1. Clonar e instalar as dependências

```bash
git clone <repo-url>
cd orders_management
poetry install
```

> **Se o seu Python padrão for menor que 3.12** (ex.: `python3 --version` mostra 3.10), o `poetry install` vai falhar com `The currently activated Python version ... is not supported`. Diga ao Poetry para usar a 3.12 explicitamente antes de instalar:
> ```bash
> poetry env use python3.12
> poetry install
> ```
> No Windows, use o caminho do `py` launcher, ex.: `poetry env use py -3.12` ou `poetry env use "C:\Python312\python.exe"`.

### 2. Configurar as variáveis de ambiente

Copie o exemplo abaixo para um arquivo `.env` na raiz do projeto (veja [Variáveis de Ambiente](#variáveis-de-ambiente)).

### 3. Criar o banco de dados

Essa etapa tem duas partes bem diferentes, que costumam ser confundidas:

1. **Uma vez só, como o superusuário `postgres`**, para criar o usuário/role da aplicação (`orders_app`) e os bancos — é aqui que o `sudo` aparece.
2. **No dia a dia, como o próprio `orders_app`**, para rodar migrações, o seed, ou inspecionar dados manualmente — aqui **não precisa de `sudo`**.

#### 3.1 Uma vez só: acessar como `postgres` e criar o usuário da aplicação

- **Linux:** o PostgreSQL costuma criar um usuário de sistema `postgres` sem senha, que só autentica via socket local ("peer authentication") — por isso o `sudo -u postgres` (roda o `psql` como esse usuário de sistema), e não porque o Postgres em si exija privilégios de root:
  ```bash
  sudo -u postgres psql
  ```
- **macOS (Homebrew):** normalmente seu usuário já é superusuário do Postgres, então basta (sem `sudo`):
  ```bash
  psql postgres
  ```
- **Windows:** use o utilitário `psql` incluído na instalação (ex.: via "SQL Shell (psql)" no menu iniciar, ou o `psql` do PATH), conectando como o usuário `postgres` criado no instalador (sem `sudo`, que não existe no Windows):
  ```bash
  psql -U postgres
  ```
  (ele vai pedir a senha definida durante a instalação do PostgreSQL)

Dentro do prompt do `psql`, crie o usuário e os bancos de dados:

```sql
CREATE USER orders_app WITH PASSWORD 'sua-senha-aqui';
CREATE DATABASE orders_management OWNER orders_app;
CREATE DATABASE orders_management_test OWNER orders_app;
\q
```

Use esse mesmo usuário e senha no `DATABASE_URL` e `DATABASE_URL_TEST` do seu `.env`, por exemplo:

```env
DATABASE_URL=postgresql://orders_app:sua-senha-aqui@localhost/orders_management
```

> **Erro comum (Linux/macOS):** rodar apenas `createdb orders_management` sem um usuário configurado costuma falhar com `role "<seu-usuário-do-sistema>" does not exist`. Isso acontece porque `createdb` tenta se conectar usando o nome do seu usuário do sistema operacional como role do Postgres. Criar o usuário `orders_app` acima evita esse problema.

#### 3.2 No dia a dia: acessar como `orders_app` (sem `sudo`)

Depois que o usuário `orders_app` existe, você **não precisa mais de `sudo` nem do usuário `postgres`** para nada — nem a aplicação, nem você manualmente. Basta conectar informando o host, para forçar autenticação por senha em vez de "peer":

```bash
psql -h localhost -U orders_app -d orders_management
```

Ele vai pedir a senha definida no `CREATE USER` acima. O `sudo -u postgres psql` do passo 3.1 é só para tarefas administrativas pontuais (criar/remover usuários e bancos) — no uso normal do projeto (migrações, seed, `TRUNCATE`, etc., mais abaixo neste README) sempre se conecta como `orders_app`.

#### (Opcional) Conectar com pgAdmin ou DBeaver

Para visualizar as tabelas e os dados do banco de forma gráfica, você pode conectar um cliente como [pgAdmin](https://www.pgadmin.org/) ou [DBeaver](https://dbeaver.io/) usando uma nova conexão com as seguintes informações:

| Campo | Valor |
| --- | --- |
| Host | `localhost` |
| Porta | `5432` |
| Usuário | `orders_app` |
| Senha | a senha definida no `CREATE USER` acima |
| Banco de dados | `orders_management` |

Isso é totalmente opcional — a aplicação não depende desses clientes para funcionar —, mas é útil para conferir visualmente se as migrações (passo 4) e o seed (passo 5) rodaram corretamente.

### 4. Executar as migrações do banco de dados

Este repositório **não versiona os arquivos de migração** (pasta `migrations/versions/`) — cada pessoa gera as suas localmente a partir dos modelos atuais. Na primeira vez que configurar o projeto, gere a migração inicial antes de aplicá-la:

```bash
poetry run alembic revision --autogenerate -m "initial migration"
poetry run alembic upgrade head
```

Depois da primeira vez, para aplicar migrações já existentes (ex.: depois de um `git pull` que não trouxe mudanças nos modelos), basta:

```bash
poetry run alembic upgrade head
```

Se você alterar algum modelo em `app/models/models.py`, gere uma nova migração com `alembic revision --autogenerate -m "descreva sua mudança"` e rode `alembic upgrade head` novamente (veja [Migrações do Banco de Dados](#migrações-do-banco-de-dados)).

### 5. (Opcional) Popular os produtos

```bash
poetry run python scripts/seed_products.py
```

### 6. Iniciar o servidor de desenvolvimento

```bash
poetry run task dev
```

A API ficará disponível em `http://localhost:8000`.

---

## Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes chaves:

```env
# Banco de dados principal
DATABASE_URL=postgresql://<usuario>:<senha>@localhost/orders_management

# Banco de dados de testes (se usar pytest)
DATABASE_URL_TEST=postgresql://<usuario>:<senha>@localhost/orders_management_test

# Chave secreta para assinatura do JWT
SECRET_KEY=your-secret-key

```

---

## Migrações do Banco de Dados

As migrações são gerenciadas com Alembic. A pasta `migrations/versions/` é ignorada pelo git (veja `.gitignore`) — cada pessoa gera suas próprias migrações localmente, a partir do estado atual dos modelos (ver [passo 4](#4-executar-as-migrações-do-banco-de-dados) para a primeira migração).

```bash
# Aplica todas as migrações pendentes
poetry run alembic upgrade head

# Cria uma nova migração (gerada automaticamente a partir das mudanças nos modelos)
poetry run alembic revision --autogenerate -m "descreva sua mudança"

# Reverte a última migração
poetry run alembic downgrade -1
```

---

## Populando o Banco de Dados

Um script de seed lê `scripts/products.json` e insere cada item na tabela `products`. Execute-o depois que as migrações tiverem sido aplicadas:

```bash
poetry run python scripts/seed_products.py
```

Se tudo der certo, você verá:

```
6 products inserted successfully
```

### Formato do JSON

Cada objeto em `scripts/products.json` corresponde diretamente ao modelo `Product`:

```json
[
  {
    "name": "Mechanical Keyboard",
    "description": "TKL layout, Cherry MX switches.",
    "price": 289.90
  },
  {
    "name": "Webcam 1080p",
    "description": null,
    "price": 199.00
  }
]
```

| Campo | Tipo | Obrigatório | Observações |
|---|---|---|---|
| `name` | string | Sim | Nome de exibição do produto |
| `description` | string \| null | Não | Descrição curta; omita ou use `null` para deixar em branco |
| `price` | number | Sim | Valor decimal na moeda local |

### Personalizando o catálogo

1. Abra `scripts/products.json`.
2. Adicione, edite ou remova itens seguindo o formato acima.
3. Execute o script novamente — ele apenas adiciona itens ao que já existe no banco, então rode-o apenas uma vez por ambiente, ou trunque a tabela `products` antes se quiser começar do zero:

```bash
# Trunca e popula novamente (psql)
psql -h localhost -U orders_app -d orders_management -c "TRUNCATE products CASCADE;"
poetry run python scripts/seed_products.py
```
