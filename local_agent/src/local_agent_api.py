from fastapi import FastAPI
from pydantic import BaseModel
import os

app = FastAPI(title="Local Agent API")

MINISTRY_ID = os.environ.get("MINISTRY_ID", "unknown")

class AccessRequestFromBroker(BaseModel):
    requester: str
    document_id: str

@app.post("/ask_leader_for_access")
async def ask_leader_for_access(req: AccessRequestFromBroker):
    """
    Принимает запрос от Глобального Брокера.
    В реальной системе здесь агент пишет руководителю в чат (OpenClaw) и ждет ответа (Human-in-the-Loop).
    Для прототипа имитируем логику: даем разовый доступ.
    """
    print(f"[{MINISTRY_ID.upper()} AGENT] ВНИМАНИЕ РУКОВОДИТЕЛЮ:")
    print(f"[{MINISTRY_ID.upper()} AGENT] Министерство {req.requester} запрашивает доступ к нашему документу {req.document_id}.")
    
    # Имитация ответа руководителя: "разрешить разовый доступ"
    print(f"[{MINISTRY_ID.upper()} LEADER] Разрешаю разовый доступ.")
    
    # В реальной системе здесь бы доставался реальный зашифрованный вектор из локального Qdrant
    mock_document_content = "Секретные данные, расшифрованные специально для " + req.requester
    
    return {
        "status": "approved",
        "access_type": "one-time",
        "data": mock_document_content
    }
