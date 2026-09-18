# Orders Management — Frontend

Uma aplicação single-page para navegar por produtos, montar um carrinho e acompanhar pedidos. Construída com React, TypeScript e SCSS puro. Comunica-se com um backend de API REST rodando em `localhost:8000`.

> **Escopo — Entrega 1**: esta versão cobre o fluxo principal (cadastro → login → listar produtos → montar carrinho → criar pedido → ver meus pedidos). Gestão administrativa (CRUD de produto, finalizar/cancelar pedido) e a paleta de cores final ficam para a Entrega 2.

---

## Sumário

- [Visão Geral](#visão-geral)
- [Stack](#stack)
- [Pré-requisitos](#pré-requisitos)
- [Primeiros Passos](#primeiros-passos)
- [Configuração de Ambiente](#configuração-de-ambiente)
- [Scripts Disponíveis](#scripts-disponíveis)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Páginas e Funcionalidades](#páginas-e-funcionalidades)
- [Autenticação](#autenticação)
- [Camada de API](#camada-de-api)
- [Escopo da Entrega 1](#escopo-da-entrega-1)

---

## Visão Geral

Orders Management é uma aplicação de fluxo de pedidos de e-commerce. Usuários se cadastram, navegam pelos produtos, montam um carrinho de compras e acompanham seus pedidos.

---

## Stack

| Camada | Tecnologia |
|---|---|
| Framework | React 19 |
| Linguagem | TypeScript 6 |
| Ferramenta de build | Vite 8 |
| Roteamento | React Router DOM 7 |
| Cliente HTTP | Axios 1 |
| Estilização | SCSS puro (CSS Modules + `sass`) |
| Linting | ESLint 10 com TypeScript ESLint |

---

## Pré-requisitos

- Node.js 18 ou superior
- npm 9 ou superior
- Uma instância em execução da API backend em `http://localhost:8000`

---

## Primeiros Passos

**1. Clone o repositório**

```bash
git clone <repository-url>
cd Front
```

**2. Instale as dependências**

```bash
npm install
```

**3. Inicie o servidor de desenvolvimento**

```bash
npm run dev
```

A aplicação ficará disponível em `http://localhost:5173` por padrão.

---

## Configuração de Ambiente

A URL base da API está atualmente fixa (hardcoded) em [`src/services/api.ts`](src/services/api.ts):

```ts
const api = axios.create({
  baseURL: "http://localhost:8000",
});
```

Para apontar para um backend diferente, atualize `baseURL` diretamente nesse arquivo, ou refatore para ler a partir de uma variável de ambiente (ex.: `import.meta.env.VITE_API_URL`).

---

## Scripts Disponíveis

| Script | Descrição |
|---|---|
| `npm run dev` | Inicia o servidor de desenvolvimento do Vite com hot module replacement |
| `npm run build` | Verifica os tipos e compila um bundle de produção em `dist/` |
| `npm run preview` | Serve o bundle de produção localmente para verificação |
| `npm run lint` | Executa o ESLint em todo o projeto |

---

## Estrutura do Projeto

```
src/
  components/
    PrivateRoute.tsx     # Redireciona usuários não autenticados para /login
    UI.tsx               # Primitivas de UI compartilhadas (Layout, Button, PageHeader, etc.)
  context/
    AuthContext.tsx      # Estado de autenticação, persistência do token, flag isAdmin
  pages/
    Login/
      Login.tsx          # Formulário de login
    Register/
      Register.tsx       # Formulário de criação de conta com validação no cliente
    Products/
      Products.tsx       # Listagem de produtos com ação de adicionar ao carrinho
      ProductDetail.tsx  # Visualização de um único produto com seletor de quantidade
    Cart/
      Cart.tsx           # Revisão do carrinho, gerenciamento de quantidade e finalização do pedido
    Orders/
      Orders.tsx         # Histórico de pedidos com itens expansíveis
  services/
    api.ts               # Instância do Axios com interceptor de token Bearer
    auth.ts               # register, login, logout, me
    products.ts            # getAllProducts, getProduct
    cart.ts                 # Leitura do carrinho e gerenciamento de itens
    orders.ts               # createOrder, getAllOrders, getOrder
  styles/
    _variables.scss       # Única fonte de cor/layout
    _mixins.scss
  types/
    types.ts              # Interfaces TypeScript compartilhadas (User, Product, Cart, Order, etc.)
  App.tsx                 # Definições de rotas
  main.tsx                # Ponto de entrada do React
```

---

## Páginas e Funcionalidades

### `/login` — Login

- Aceita nome de usuário ou e-mail junto com a senha.
- Em caso de sucesso, salva o JWT no `localStorage` e redireciona para `/products`.

### `/register` — Criar conta

- Coleta nome de usuário, e-mail e senha (mínimo de 8 caracteres).
- Valida todos os campos no cliente antes de fazer a chamada à API.
- Em caso de sucesso, autentica o usuário imediatamente e redireciona para `/products`.

### `/products` — Listagem de produtos

- Exibe todos os produtos em um grid responsivo.
- Cada card tem um botão **Add to cart**, com uma breve confirmação visual ("Added").
- Clicar em um card de produto leva à página de detalhes.

### `/products/:id` — Detalhe do produto

- Mostra o nome, a descrição e o preço do produto.
- Inclui um seletor de quantidade que atualiza o total em tempo real.
- Um botão **Adicionar ao carrinho** adiciona a quantidade selecionada.

### `/cart` — Carrinho de compras

- Lista todos os itens com controles de quantidade e subtotais por item.
- Passar o mouse sobre uma linha revela um botão de remover.
- Um painel de resumo do pedido à direita mostra os totais individuais e o total geral do carrinho.
- Clicar em **Finalizar pedido** converte o carrinho em um novo pedido e redireciona para `/orders`.

### `/orders` — Histórico de pedidos

- Lista todos os pedidos como linhas expansíveis, mostrando ID do pedido, data, status e total.
- Expandir uma linha revela o detalhamento dos itens.

---

## Autenticação

A autenticação é baseada em token, usando JWT Bearer tokens.

- Após um login ou cadastro bem-sucedido, o token de acesso é salvo no `localStorage` sob a chave `token`.
- A instância do Axios em [`src/services/api.ts`](src/services/api.ts) anexa automaticamente o token como um cabeçalho `Authorization: Bearer <token>` em cada requisição.
- Ao carregar a página, o [`AuthContext`](src/context/AuthContext.tsx) lê o token do `localStorage`, chama `GET /auth/me` para restaurar a sessão do usuário, e limpa o token caso a chamada falhe (por exemplo, token expirado).
- O componente [`PrivateRoute`](src/components/PrivateRoute.tsx) envolve todas as rotas autenticadas. O acesso não autenticado é redirecionado para `/login`.
- O `AuthContext` já expõe um booleano `isAdmin` (derivado de `user.role`), usado hoje só para variar o subtítulo da página de pedidos — os controles administrativos que dependeriam dele chegam na Entrega 2.

---

## Camada de API

Todas as funções de serviço ficam em `src/services/` e são agrupadas por domínio. Elas retornam promises tipadas que correspondem às interfaces em [`src/types/types.ts`](src/types/types.ts).

| Arquivo | Endpoints utilizados |
|---|---|
| `auth.ts` | `POST /auth/register`, `POST /auth/login`, `GET /auth/me` |
| `products.ts` | `GET /products`, `GET /products/:id` |
| `cart.ts` | `GET /cart`, `POST /cart/items`, `PUT /cart/items/:id`, `DELETE /cart/items/:id` |
| `orders.ts` | `GET /orders`, `GET /orders/:id`, `POST /orders` |

---

## Escopo da Entrega 1

Esta entrega cobre só a funcionalidade principal: cadastro → login → listar produtos → montar carrinho → criar pedido → ver meus pedidos. Gestão administrativa fica para a Entrega 2:

- **CRUD de produtos** (criar/editar/excluir) — sem rota no backend nem UI no front nesta entrega.
- **Finalizar / cancelar pedido** — sem rota no backend nem ações na página de pedidos nesta entrega.

A aplicação também usa uma **paleta de cores neutra/genérica** nesta entrega.