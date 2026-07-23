from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import os

app = FastAPI(title="Global Broker API")

# Registry of local agents (in a real scenario, this would be dynamic via service discovery)
# Реестр агентов (будет динамически заполняться при подключении реальных министерств)
# Для прототипа используем универсальное имя контейнера local_agent_api
AGENT_REGISTRY = {
    "min_energo": "http://local_agent_api:8000",
    "min_stroy": "http://local_agent_api:8000",
    "min_example": "http://local_agent_api:8000"
}

class SearchRequest(BaseModel):
    query: str
    requester_ministry: str

class AccessRequest(BaseModel):
    requester_ministry: str
    target_ministry: str
    document_id: str

@app.post("/search")
async def global_search(req: SearchRequest):
    """
    1. Ищет данные в Глобальном Qdrant.
    2. Если данные чужие и закрытые (имитация), предлагает сделать запрос доступа.
    """
    # Мок поиска
    print(f"[BROKER] Поиск '{req.query}' для {req.requester_ministry}")
    
    # Имитируем, что мы нашли документ, принадлежащий другому министерству
    target = "minstroy" if req.requester_ministry == "minenergo" else "minenergo"
    
    return {
        "status": "found_locked",
        "message": f"Найден релевантный документ у {target}, но он закрыт.",
        "document_id": f"doc_{target}_123",
        "owner": target
    }

@app.post("/request_access")
async def request_access(req: AccessRequest):
    """
    Маршрутизирует запрос на доступ к целевому агенту
    """
    print(f"[BROKER] Брокеридж: {req.requester_ministry} просит доступ к {req.document_id} у {req.target_ministry}")
    
    target_url = AGENT_REGISTRY.get(req.target_ministry)
    if not target_url:
        raise HTTPException(status_code=404, detail="Target agent not found")
        
    async with httpx.AsyncClient() as client:
        try:
            # Отправляем зашифрованный (в теории) запрос целевому агенту
            response = await client.post(
                f"{target_url}/ask_leader_for_access",
                json={"requester": req.requester_ministry, "document_id": req.document_id}
            )
            return response.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
