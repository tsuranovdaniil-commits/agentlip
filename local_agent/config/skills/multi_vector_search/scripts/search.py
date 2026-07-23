import argparse
import sys
import requests
import os

def federated_search(query, ministry):
    global_broker_url = os.environ.get("GLOBAL_BROKER_URL", "http://localhost:8000")
    
    print(f"[LOCAL AGENT {ministry.upper()}] Ищу '{query}' в своей локальной базе...")
    print(f"[LOCAL AGENT {ministry.upper()}] Не нашел. Отправляю запрос Глобальному Брокеру...")
    
    try:
        # Запрос к брокеру
        res = requests.post(f"{global_broker_url}/search", json={
            "query": query,
            "requester_ministry": ministry
        }).json()
        
        if res.get("status") == "found_locked":
            print(f"\n[GLOBAL BROKER] {res['message']}")
            print(f"[LOCAL AGENT {ministry.upper()}] Спрашиваю пользователя: Запросить доступ у руководителя {res['owner']}?")
            # Имитация согласия пользователя
            print(f"[USER] Да, запроси.")
            
            # Отправка запроса на доступ
            print(f"[LOCAL AGENT {ministry.upper()}] Запрашиваю доступ через Глобального Брокера...")
            access_res = requests.post(f"{global_broker_url}/request_access", json={
                "requester_ministry": ministry,
                "target_ministry": res["owner"],
                "document_id": res["document_id"]
            }).json()
            
            if access_res.get("status") == "approved":
                print(f"\n[SUCCESS] Доступ получен ({access_res['access_type']})!")
                print(f"[DATA] Полученные зашифрованные данные: {access_res['data']}")
            else:
                print("\n[DENIED] В доступе отказано.")
                
    except Exception as e:
        print(f"[ERROR] Ошибка связи с Глобальным Брокером: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multi-Vector Search (С поддержкой брокериджа)")
    parser.add_argument("query", type=str, help="Поисковый запрос")
    parser.add_argument("--ministry", type=str, default="minenergo", help="Кто запрашивает")
    
    args = parser.parse_args()
    federated_search(args.query, args.ministry)
