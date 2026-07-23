from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import os
import uuid
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct

app = FastAPI(title="Global Broker API")

QDRANT_URL = os.environ.get("QDRANT_URL", "http://global_qdrant:6333")
try:
    qclient = QdrantClient(url=QDRANT_URL)
except Exception as e:
    print(f"Warning: Could not connect to Qdrant at {QDRANT_URL} during startup. {e}")
    qclient = None

VECTOR_SIZE = 128 # Размер вектора для прототипа (заглушка без нейросети)

def ensure_collection(name: str):
    if qclient and not qclient.collection_exists(name):
        qclient.create_collection(
            collection_name=name,
            vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
        )

# Инициализация единой публичной базы
if qclient:
    ensure_collection("global_public_knowledge")

class UploadRequest(BaseModel):
    text: str
    ministry_id: str
    is_secret: bool

class SearchRequest(BaseModel):
    query: str
    ministry_id: str

@app.post("/upload")
async def global_upload(req: UploadRequest):
    if not qclient:
        return {"error": "Qdrant is not connected"}
        
    # Маршрутизация коллекции (Вариант Б: все на глобальном, но секреты изолированы)
    collection_name = "global_public_knowledge"
    if req.is_secret:
        collection_name = f"secret_{req.ministry_id}"
        ensure_collection(collection_name)
        
    point_id = str(uuid.uuid4())
    # Заглушка вектора (в реале здесь будет вызов OpenAI/FastEmbed)
    dummy_vector = [0.1] * VECTOR_SIZE 
    
    qclient.upsert(
        collection_name=collection_name,
        points=[
            PointStruct(
                id=point_id,
                vector=dummy_vector,
                payload={"text": req.text, "owner": req.ministry_id, "is_secret": req.is_secret}
            )
        ]
    )
    return {"status": "success", "collection": collection_name, "id": point_id}

@app.post("/search")
async def global_search(req: SearchRequest):
    if not qclient:
        return {"error": "Qdrant is not connected"}
        
    dummy_vector = [0.1] * VECTOR_SIZE
    
    # 1. Поиск по общей публичной базе
    public_results = qclient.search(
        collection_name="global_public_knowledge",
        query_vector=dummy_vector,
        limit=3
    )
    
    # 2. Поиск по своей изолированной секретной базе (если есть)
    secret_col = f"secret_{req.ministry_id}"
    secret_results = []
    if qclient.collection_exists(secret_col):
        secret_results = qclient.search(
            collection_name=secret_col,
            query_vector=dummy_vector,
            limit=3
        )
        
    def format_result(hits):
        return [{"text": h.payload.get("text"), "score": round(h.score, 2)} for h in hits]
        
    return {
        "status": "success",
        "public_knowledge": format_result(public_results),
        "own_secret_knowledge": format_result(secret_results)
    }
