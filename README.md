# AgentLip

Проект `tsdanlip/agentlip` с автоматической сборкой и деплоем в Docker Hub через GitHub Actions.

## CI/CD Pipeline
При каждом пуше в ветку `main` запускается workflow `.github/workflows/docker-publish.yml`:
1. Авторизация в Docker Hub.
2. Сборка Docker-образа.
3. Публикация в `tsdanlip/agentlip:latest`.
