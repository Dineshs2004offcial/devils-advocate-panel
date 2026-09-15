# Deployment

## Local Development

### Backend

```bash
cd backend
pip install -r requirements.txt
```

Start the FastAPI application using the project's configured command.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Environment Variables

Use `.env.example` as the template for the project's required variables.

Never commit `.env` or API keys to GitHub.

## Production

```text
GitHub
  |
  +--> Backend service
  +--> Frontend service
  +--> PostgreSQL
  +--> External AI/tool services
```

Configure production secrets through the hosting provider.
