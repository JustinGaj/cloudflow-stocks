from fastapi import FastAPI
from fastapi.responses import JSONResponse
import os
from app import etl

app = FastAPI(title="CloudFlowStocks API")

DATA_PATH = os.getenv("DATA_PATH", "/app/data/sample.csv")

@app.on_event("startup")
def startup_event():
    # Ensure data exists
    if not os.path.exists(DATA_PATH):
        app.state.data = []
    else:
        app.state.data = etl.load_processed(DATA_PATH)

@app.get("/api/top")
def get_top(n: int = 10):
    """Return top n stocks by percent_change or other metric"""
    data = app.state.data
    top = etl.top_n(data, n)
    return JSONResponse(content={"top": top})

@app.get("/health")
def health():
    return {"status": "ok"}
