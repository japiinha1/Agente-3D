from fastapi import FastAPI

app = FastAPI(title="Agente 3D")

@app.get("/health")
def health():
    return {"status": "ok"}

