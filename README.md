# Tomo

A minimal Pomodoro timer. Start a 25-minute timer; each finished or stopped session is saved and listed.

```
Browser ──> CloudFront ──┬── /*      ──> S3 (frontend)
                         └── /api/*  ──> API Gateway ──> Lambda (backend) ──> DynamoDB
```

- `frontend/`: Svelte + Vite static site
- `backend/`: FastAPI on Python 3.13, with Lambda handler `app.main.handler`

## API

| Method | Path | |
|---|---|---|
| GET | `/api/health` | `{"status": "ok"}` |
| GET | `/api/sessions` | Sessions, newest first |
| POST | `/api/sessions` | `{"started_at": "2026-09-30T08:00:00Z", "duration_sec": 1500}` |

## Run locally

Requires [uv](https://docs.astral.sh/uv/) and [Bun](https://bun.sh).

```sh
cd frontend && bun install && bun run dev   # http://localhost:5173
```

## Test

```sh
cd backend && uv run ruff check . && uv run pytest
cd frontend && bun install && bun run check && bun run build
```

## Terraform

See [terraform/README.md](terraform/README.md)
