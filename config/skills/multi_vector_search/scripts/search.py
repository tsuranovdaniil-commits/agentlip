import argparse
import sys
import json
import os

def federated_search(query, ministry):
    local_qdrant_url = os.environ.get("LOCAL_QDRANT_URL", "http://localhost:6333")
    global_qdrant_url = os.environ.get("GLOBAL_QDRANT_URL", "http://global-brain:6333")
    
    print(f"[SEARCH] Выполняю Федеративный поиск по запросу: '{query}'")
    print(f"[SEARCH] 1. Запрос в Локальный узел: {local_qdrant_url} (Все данные для {ministry})")
    
    # Псевдо-код запроса:
    # local_results = qdrant_client_local.search(collection_name="knowledge", query_vector=vec)
    local_results = [
        {"id": 1, "text": "Локальный секретный документ...", "security_level": "secret", "source": "local"}
    ]
    
    print(f"[SEARCH] 2. Запрос в Глобальный мозг: {global_qdrant_url} (Только public данные)")
    # Псевдо-код запроса:
    # global_results = qdrant_client_global.search(collection_name="global_knowledge", query_vector=vec, query_filter={"security_level": "public"})
    global_results = [
        {"id": 2, "text": "Публичный отчет министерства строительства...", "security_level": "public", "source": "global"}
    ]
    
    # Объединение
    all_results = local_results + global_results
    
    print("\n[РЕЗУЛЬТАТЫ ПОИСКА]")
    for res in all_results:
        print(f"[{res['source'].upper()}] ({res['security_level']}): {res['text']}")
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multi-Vector Search (Локальный + Глобальный)")
    parser.add_argument("query", type=str, help="Поисковый запрос")
    parser.add_argument("--ministry", type=str, default="unknown", help="Имя министерства, от лица которого идет запрос")
    
    args = parser.parse_args()
    federated_search(args.query, args.ministry)
