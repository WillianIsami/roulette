# Project Documentation

## 1. Overview

Roulette Royale is a full-stack roulette simulation platform with:

- Django REST backend for authentication, bet validation, wallet and transactions
- Vue 3 frontend with responsive roulette table, chip selection and wallet panel
- JWT cookie auth (`access_token` + `refresh_token`)
- Automated test suite and GitHub Actions CI

## 2. Architecture

### Backend (`server/api`)

- Framework: Django + Django REST Framework
- Authentication: SimpleJWT with HTTP-only cookies
- Main app: `roulette_api`
- Persistent entities:
  - `Wallet` (one per user)
  - `Transaction` (credits/debits for deposit/win/loss)

### Frontend (`frontend`)

- Framework: Vue 3
- Router: Vue Router (guarded routes)
- State: Vuex module (`auth`)
- API integration: `fetch` + `axios`
- Main gameplay UI: `Wheel.vue` + `RouletteBorder.vue`

## 3. Bet Engine Rules

All bets are validated server-side before applying wallet changes.

### Validation behavior

- Rejects malformed bets (`[value, type, numbers]` required)
- Rejects unknown bet types
- Rejects invalid number combinations per roulette rule set
- Rejects out-of-range numbers (must be `0..36`)
- Rejects spin if wallet balance is lower than total stake

### Payout model

Profit formula used on win:

- `profit = (36 / covered_numbers) * value - value`

Examples:

- Straight-up (1 number): `35:1`
- Split (2): `17:1`
- Street (3): `11:1`
- Corner (4): `8:1`
- Two Street (6): `5:1`
- Dozen/Line (12): `2:1`
- Even-money bets (18): `1:1`

## 4. API Endpoints

### Auth

- `POST /api/create/` - create user
- `POST /api/token/` - login and set cookies
- `POST /api/token/refresh/` - refresh auth cookies
- `POST /api/logout/` - clear auth cookies
- `GET /api/is-authenticated/` - auth check

### Betting

- `GET /api/` - list available bets
- `POST /api/spin/` - resolve spin for selected bets

### Wallet

- `GET /api/wallet/?limit=10` - wallet summary + latest transactions
- `POST /api/wallet/deposit/` - add virtual coins
- `GET /api/transactions/?limit=20` - list transaction history

## 5. Frontend Flows

### Login/Register

- `RegisterView` creates account through API
- `LoginView` authenticates and redirects to home
- Route guard blocks `/` and `/bets` unless authenticated

### Betting UX

- Choose chip value (`5, 10, 25, 50, 100`)
- Click table sectors (inside and outside bets)
- See current selected bets and total stake
- Spin and receive detailed response (`drawn_number`, `net_result`, `new_balance`)

### Wallet UX

- Quick deposits (`+100`, `+500`, `+1000`)
- Live wallet balance
- Latest transactions panel

## 6. Design Direction

Visual refresh is based on casino cues:

- Green felt + gold accents
- Rounded glass panels and clear hierarchy
- Responsive grid and horizontal-safe table area

Reference sources:

- https://dribbble.com/search/roulette
- https://www.shutterstock.com/pt/search/roulette-table-layout?dd_referrer=https%3A%2F%2Fwww.google.com%2F

## 7. Tests and Quality

### Backend

- Location: `server/api/roulette_api/tests`
- Includes roulette rules, API, wallet and transaction tests
- Run with:

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

## 8. CI (GitHub Actions)

Workflow file: `.github/workflows/django-server.yml`

- Frontend job:
  - `npm ci`
  - `npm run lint`
  - `npm run build`
- Backend job:
  - `uv venv .venv`
  - `uv pip install -r requirements.txt`
  - `USE_SQLITE=true uv run python manage.py test`

## 8.1 Backend Dependency Management (Recommended)

Use `uv` to avoid global Python dependency conflicts:

```bash
cd server/api
uv venv .venv
uv pip install -r requirements.txt
USE_SQLITE=true uv run python manage.py migrate
USE_SQLITE=true uv run python manage.py runserver 0.0.0.0:8080
```

## 9. Screenshots Automation

Script:

- `frontend/scripts/captureScreenshots.mjs`

Behavior:

- Captures the app shell of each route (`header + main + footer`) with outer margin (no full browser-page screenshot), reducing empty space.

Command:

```bash
cd frontend
npm run capture:screenshots -- --base-url=http://localhost:8000 --api-url=http://localhost:8080
```

Generated files:

- `docs/screenshots/*.png`
