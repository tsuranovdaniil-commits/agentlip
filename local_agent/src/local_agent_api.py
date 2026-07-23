from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import os

app = FastAPI(title="Local Agent API")

MINISTRY_ID = os.environ.get("MINISTRY_ID", "unknown")
GLOBAL_BROKER_URL = os.environ.get("GLOBAL_BROKER_URL", "http://global_broker:8000")

class AgentSyncRequest(BaseModel):
    text: str
    is_secret: bool

class AgentSearchRequest(BaseModel):
    query: str

@app.post("/agent/sync")
async def agent_sync(req: AgentSyncRequest):
    """
    OpenClaw агент (ИИ) вызывает этот метод для сохранения информации.
    API обогащает запрос токеном министерства и шлет в Глобальный Брокер.
    """
    async with httpx.AsyncClient() as client:
        payload = {
            "text": req.text,
            "ministry_id": MINISTRY_ID,
            "is_secret": req.is_secret
        }
        try:
            resp = await client.post(f"{GLOBAL_BROKER_URL}/upload", json=payload)
            return resp.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Broker connection failed: {e}")

@app.post("/agent/search")
async def agent_search(req: AgentSearchRequest):
    """
    OpenClaw агент вызывает этот метод для поиска информации по всей федеративной сети.
    """
    async with httpx.AsyncClient() as client:
        payload = {
            "query": req.query,
            "ministry_id": MINISTRY_ID
        }
        try:
            resp = await client.post(f"{GLOBAL_BROKER_URL}/search", json=payload)
            return resp.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Broker connection failed: {e}")
