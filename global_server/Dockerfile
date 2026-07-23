# Stage 1: Сборка (Компиляция Python в бинарный C-код)
FROM python:3.10-slim as builder

WORKDIR /app
# Устанавливаем компилятор C
RUN apt-get update && apt-get install -y gcc python3-dev

# Устанавливаем зависимости и Cython
COPY requirements.txt .
RUN pip install --no-cache-dir cython -r requirements.txt

# Копируем исходный код и компилируем его в бинарный .so
COPY src/global_broker.py /app/main.py
RUN cythonize -i -3 /app/main.py
# Удаляем исходный текстовый код, чтобы он случайно не попал дальше
RUN rm /app/main.py /app/main.c

# Stage 2: Финальный образ (Только бинарники, без исходников)
FROM python:3.10-slim

WORKDIR /app
# Устанавливаем обычные зависимости (без Cython и gcc, чтобы образ был легким)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем ИСКЛЮЧИТЕЛЬНО скомпилированный бинарный файл (.so)
COPY --from=builder /app/*.so /app/

# Запускаем Uvicorn (он умеет читать .so библиотеки как обычные модули)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
