# Используем официальный образ Python 3.12
FROM python:3.12-slim

# Устанавливаем зависимости для работы системы
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential=12.9 gcc=4:11.3.0-1 \
    libgl1=1.3.2-1 libglib2.0-0=2.72.4-1 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Указываем рабочую директорию
WORKDIR /app

# Копируем зависимости (requirements.txt) в контейнер
COPY requirements.txt .

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в контейнер
COPY . .

# Открываем порт для FastAPI (по умолчанию 8000)
EXPOSE 8000

# Указываем команду для запуска приложения
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]