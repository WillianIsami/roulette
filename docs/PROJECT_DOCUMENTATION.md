# Project Documentation

## 1. Overview

Roulette Royale is a full-stack roulette simulation platform with:

- Django REST backend for authentication, bet validation, wallet, and transactions
- Vue 3 frontend with responsive roulette board, chip selection, and wallet panel
- JWT cookie authentication (`access_token` + `refresh_token`)
- Full multilingual UI (`en`, `pt-BR`, `es`)
- Localized transaction descriptions rendered in the currently selected language
- Automated test suite and GitHub Actions CI

## 2. Architecture

### Backend (`server/api`)

- Framework: Django + Django REST Framework
- Authentication: SimpleJWT with HTTP-only cookies
- Main app: `roulette_api`
- Persistent entities:
  - `Wallet` (one per user)
  - `Transaction` (credits/debits for deposit/win/loss)

#### Transaction localization model

Each transaction now stores:

- `description` (human-readable fallback)
- `description_key` (stable key, e.g. `transaction.bet_win`)
- `description_context` (structured metadata for interpolation)

This allows the frontend to translate the same transaction row into any supported language without re-fetching rewritten text from backend.

### Frontend (`frontend`)

- Framework: Vue 3
- Router: Vue Router (guarded routes)
- State: Vuex (`auth` module)
- Internationalization: Vue I18n + persisted locale
- API integration: `fetch` + `axios`
- Main gameplay UI: `Wheel.vue` + `RouletteBorder.vue`

## 3. Bet Engine Rules

All bets are validated server-side before applying wallet changes.

### Validation behavior

- Reject malformed bets (`[value, type, numbers]` required)
- Reject unknown bet types
- Reject invalid number combinations per roulette rules
- Reject out-of-range numbers (`0..36`)
- Reject spin when wallet balance is lower than total stake

### Payout model

Profit formula on a winning bet:

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
- `GET /api/transactions/?limit=20` - paginated transaction history

## 5. Frontend Flows

### Login / Register

- `RegisterView` creates account through API
- `LoginView` authenticates and redirects to home
- Route guard blocks `/` and `/bets` unless authenticated

### Betting UX

- Choose chip value (`5, 10, 25, 50, 100`)
- Click roulette board sectors (inside and outside bets)
- Track selected bets with total stake
- Spin and receive full response (`drawn_number`, `net_result`, `new_balance`)

### Wallet UX

- Quick deposits (`+100`, `+500`, `+1000`)
- Live wallet balance
- Transaction panel with search, pagination, and infinite-scroll trigger

### Language UX

- Language selector in navbar (`English`, `Português (Brasil)`, `Español`)
- Locale persisted in browser storage
- All main UI text translated
- Errors and transaction descriptions translated from keys/context

## 6. Design Direction

Visual refresh follows casino references:

- Green felt + gold accents
- Rounded panels with clear hierarchy
- Responsive board and overflow-safe table container

Reference sources:

- https://dribbble.com/search/roulette
- https://www.shutterstock.com/pt/search/roulette-table-layout?dd_referrer=https%3A%2F%2Fwww.google.com%2F

## 7. Tests and Quality

### Backend

- Location: `server/api/roulette_api/tests`
- Coverage includes roulette rules, API, wallet, and transaction behavior
- Run:

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

## 9. Dependency Management with UV

Recommended backend flow to avoid global Python dependency conflicts:

```bash
cd server/api
uv venv .venv
uv pip install -r requirements.txt
USE_SQLITE=true uv run python manage.py migrate
USE_SQLITE=true uv run python manage.py runserver 0.0.0.0:8080
```

## 10. Screenshot Automation

Script:

- `frontend/scripts/captureScreenshots.mjs`

Behavior:

- Captures app shell (`header + main content + footer`) with external margin
- Waits for route data loading before capture
- Avoids full-browser-page screenshots with large empty areas

Command:

```bash
cd frontend
npm run capture:screenshots -- --base-url=http://localhost:8000 --api-url=http://localhost:8080
```

Generated files:

- `docs/screenshots/*.png`
