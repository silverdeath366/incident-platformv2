# Incident Platform

A minimal FastAPI-based incident backend with local Docker Compose and a Helm chart for Kubernetes deployment.

## Features

- FastAPI service with sample endpoints: `/health` and `/incidents`
- Dockerfile for containerization
- Docker Compose for local development
- Helm chart (`incident-backend/`) for Kubernetes deployment

## Project Structure

```
.
├─ backend/
│  ├─ app/
│  │  └─ main.py
│  ├─ Dockerfile
│  └─ requirements.txt
├─ docker-compose.yml
└─ incident-backend/               # Helm chart
   ├─ Chart.yaml
   ├─ values.yaml
   └─ templates/
      ├─ deployment.yaml
      └─ service.yaml
```

## Prerequisites

- Python 3.11+
- Docker and Docker Compose
- (Optional) Kubernetes cluster and `helm` CLI for deployment

## Running Locally (without Docker)

1. Create and activate a virtual environment
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
   ```
2. Install dependencies
   ```bash
   pip install -r backend/requirements.txt
   ```
3. Start the API
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --app-dir backend
   ```

Visit http://localhost:8000/health and http://localhost:8000/incidents

Open API docs at http://localhost:8000/docs

## Running with Docker Compose (recommended)

Build and start the backend service:

```bash
docker compose up --build
```

The API will be available at http://localhost:8000

## API Endpoints

- `GET /health` → `{ "status": "ok" }`
- `GET /incidents` → Sample list of incidents

## Container Image

`backend/Dockerfile` builds a Python 3.11-slim image and runs `uvicorn`:

```Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY ./app /app/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build locally (without Compose):

```bash
docker build -t incident-backend:local ./backend
docker run --rm -p 8000:8000 incident-backend:local
```

## Kubernetes Deployment (Helm)

The Helm chart is under `incident-backend/`.

1. Set your image repository in `incident-backend/values.yaml`:
   ```yaml
   image:
     repository: <your-docker-repo>/incident-backend
     tag: latest
     pullPolicy: Always
   ```
2. Package/push your image, then install the chart:
   ```bash
   helm upgrade --install incident-backend ./incident-backend \
     --namespace incidents --create-namespace
   ```
3. Port-forward to access the service (if using ClusterIP):
   ```bash
   kubectl -n incidents port-forward svc/incident-backend 8080:80
   # Then open http://localhost:8080/health
   ```

`values.yaml` also lets you set `replicaCount`, resources, `service.type`, and env vars.

## Development Notes

- Code lives in `backend/app/main.py`. Modify or add routes here.
- Auto-reload is enabled when running locally with `--reload`.
- API docs are served by FastAPI at `/docs`.
