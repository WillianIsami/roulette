# Roulette Royale

Plataforma completa de roleta com backend Django e frontend Vue, incluindo:

- validação real de apostas no servidor
- carteira virtual com depósito e histórico de transações
- autenticação JWT por cookie HTTP-only
- interface renovada, responsiva e otimizada para apostar
- pipeline CI para lint/build/tests

## Preview

![Home](./docs/screenshots/home.png)

Mais imagens: [docs/SCREENSHOTS.md](./docs/SCREENSHOTS.md)

## Stack

### Frontend

- Vue 3
- Vue Router
- Vuex
- Bootstrap + tema customizado

### Backend

- Django
- Django REST Framework
- SimpleJWT
- DRF-YASG (Swagger/ReDoc)

## Estrutura do projeto

- `frontend/` - aplicação Vue
- `server/api/` - API Django
- `docs/` - documentação detalhada e galeria de screenshots

Documentação completa: [docs/PROJECT_DOCUMENTATION.md](./docs/PROJECT_DOCUMENTATION.md)

## Como rodar localmente (sem Docker)

## 1) Backend

```bash
cd server/api
cp .env.example .env
```

Ajuste variáveis do `.env` se necessário.
Instale o `uv` pela documentação oficial: https://docs.astral.sh/uv/getting-started/installation/

Recomendado: usar `uv` para instalar dependências no `.venv` local (sem conflito global):

```bash
uv venv .venv
uv pip install -r requirements.txt
USE_SQLITE=true uv run python manage.py migrate
USE_SQLITE=true uv run python manage.py runserver 0.0.0.0:8080
```

## 2) Frontend

Em outro terminal:

```bash
cd frontend
cp .env.example .env
npm install
npm run serve
```

Acesse:

- Frontend: `http://localhost:8000` (ou `8001` se 8000 estiver ocupado)
- API: `http://localhost:8080`
- Swagger: `http://localhost:8080/swagger/`

## Como rodar com Docker

1. Copie os arquivos de ambiente:

```bash
cp server/api/.env.example server/api/.env
cp frontend/.env.example frontend/.env
```

2. Para Docker, use `DB_HOST=db` em `server/api/.env`.

3. Suba tudo:

```bash
docker compose up --build
```

## Testes

### Backend (todos os testes)

```bash
cd server/api
USE_SQLITE=true uv run python manage.py test
```

### Frontend

```bash
cd frontend
npm run lint
npm run build
```

## Captura de screenshots (shell completo da página)

Com backend e frontend rodando:

```bash
cd frontend
npm run capture:screenshots -- --base-url=http://localhost:8000 --api-url=http://localhost:8080
```

As imagens são salvas em `docs/screenshots/` e incluem `header + conteúdo + footer` com margem externa.

## CI (GitHub Actions)

Arquivo: `.github/workflows/django-server.yml`

- Job frontend: install + lint + build
- Job backend: install + `uv run python manage.py test`

## Referências visuais utilizadas

- https://dribbble.com/search/roulette
- https://www.shutterstock.com/pt/search/roulette-table-layout?dd_referrer=https%3A%2F%2Fwww.google.com%2F
