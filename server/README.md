# Backend (Django API)

Roulette Royale backend API with:

- JWT cookie authentication
- Roulette bet validation engine
- Wallet and transaction management
- Roulette, balance, and transaction history endpoints

## Prerequisites

- Python 3.10+
- `uv` (recommended)
- Official install docs: https://docs.astral.sh/uv/getting-started/installation/

## Setup

```bash
cd api
cp .env.example .env
uv venv .venv
uv pip install -r requirements.txt
```

## Run with SQLite (dev/test)

```bash
USE_SQLITE=true uv run python manage.py migrate
USE_SQLITE=true uv run python manage.py runserver 0.0.0.0:8080
```

## Main Endpoints

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

## Tests

```bash
USE_SQLITE=true uv run python manage.py test
```
