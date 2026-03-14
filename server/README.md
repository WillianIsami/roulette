# Backend (Django API)

API da Roulette Royale com:

- autenticação JWT por cookie
- motor de validação de apostas
- carteira e transações
- endpoints de roleta, saldo e histórico

## Pré-requisitos

- Python 3.10+
- `uv` (recomendado)
- Instalação do `uv` (docs oficiais): https://docs.astral.sh/uv/getting-started/installation/

## Configuração

```bash
cd api
cp .env.example .env
uv venv .venv
uv pip install -r requirements.txt
```

## Rodar com SQLite (dev/test)

```bash
USE_SQLITE=true uv run python manage.py migrate
USE_SQLITE=true uv run python manage.py runserver 0.0.0.0:8080
```

## Endpoints principais

- `POST /api/create/`
- `POST /api/token/`
- `POST /api/logout/`
- `GET /api/is-authenticated/`
- `GET /api/`
- `POST /api/spin/`
- `GET /api/wallet/`
- `POST /api/wallet/deposit/`
- `GET /api/transactions/`
- `GET /swagger/`

## Testes

```bash
USE_SQLITE=true uv run python manage.py test
```
