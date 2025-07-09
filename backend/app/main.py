from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/incidents")
def list_incidents():
    return [
        {"id": 1, "title": "Database down", "status": "open"},
        {"id": 2, "title": "Service crash", "status": "resolved"},
    ]
