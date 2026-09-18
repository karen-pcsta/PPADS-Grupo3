# Orders Management

Um sistema simplificado de gerenciamento de pedidos de e-commerce, dividido em dois projetos:

| Pasta | O que é | Tecnologias |
|---|---|---|
| [`Back/`](Back/README.md) | API REST | FastAPI, SQLAlchemy, PostgreSQL, Alembic |
| [`Front/`](Front/README.md) | Aplicação web | React, TypeScript, Vite, SCSS |

O frontend consome a API do backend em `http://localhost:8000`. Para o sistema funcionar de ponta a ponta, **o backend precisa estar rodando antes de você abrir o frontend**.

---

## Visão Geral

Usuários podem se cadastrar, navegar pelo catálogo de produtos, montar um carrinho e finalizar pedidos. Administradores têm controles extras para gerenciar produtos e para finalizar ou cancelar qualquer pedido.

---

## Ordem de Configuração

Cada projeto tem seu próprio README com o passo a passo detalhado. Siga nesta ordem:

### 1. Configure e rode o backend primeiro

Siga o guia completo em **[Back/README.md](Back/README.md)**. Resumo do que ele cobre:

- Instalar Python 3.12+ e Poetry
- Criar o usuário e os bancos de dados no PostgreSQL
- Rodar as migrações do Alembic
- (Opcional) Popular produtos de exemplo
- Iniciar o servidor com `poetry run task dev`

Quando terminar, a API estará disponível em `http://localhost:8000`.

### 2. Depois, configure e rode o frontend

Siga o guia completo em **[Front/README.md](Front/README.md)**. Resumo do que ele cobre:

- Instalar Node.js 18+ e npm
- Instalar as dependências com `npm install`
- Iniciar o servidor com `npm run dev`

Quando terminar, a aplicação estará disponível em `http://localhost:5173`.

---

## Papéis (Roles)

A aplicação tem dois tipos de usuário:

| Capacidade | Usuário comum | Admin |
|---|---|---|
| Navegar pelos produtos, adicionar ao carrinho e fazer pedidos | Sim | Sim |
| Cancelar os próprios pedidos pendentes | Sim (Implementação entrega-2)| Sim (Implementação entrega-2)|
| Criar / editar / excluir produtos | Não | Sim (Implementação entrega-2) |
| Finalizar ou cancelar qualquer pedido | Não | Sim (Implementação entrega-2) |

---

## Problemas comuns

Antes de abrir uma issue ou pedir ajuda, veja se seu problema já está coberto:

- **Erros ao criar o banco de dados, rodar migrações ou usar o Poetry** → seção [Primeiros Passos](Back/README.md#primeiros-passos) do `Back/README.md`, que traz instruções específicas para Linux, macOS e Windows.
- **Frontend não consegue falar com a API** → confirme que o backend está rodando em `http://localhost:8000` (passo 1 acima) e veja [Configuração de Ambiente](Front/README.md#configuração-de-ambiente) no `Front/README.md`.
