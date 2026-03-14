# Frontend (Vue 3)

Interface da Roulette Royale com foco em:

- experiência de aposta responsiva
- carteira virtual com depósitos rápidos
- resumo de apostas e resultado de giro
- autenticação com rotas protegidas

## Pré-requisitos

- Node.js 18+
- backend rodando em `http://localhost:8080`

## Configuração

```bash
cp .env.example .env
npm install
```

`.env` esperado:

```env
VUE_APP_BASE_URL=http://localhost:8080
CLIENT_PORT=8000
```

## Comandos

```bash
npm run serve
npm run lint
npm run build
```

## Screenshots automáticas

```bash
npm run capture:screenshots -- --base-url=http://localhost:8000 --api-url=http://localhost:8080
```

Saída: `../docs/screenshots/` (captura `header + conteúdo + footer` com margem externa, sem screenshot da página inteira do navegador).
