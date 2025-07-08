FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./backend/
COPY frontend/ ./frontend/

EXPOSE 8000
EXPOSE 8501

ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]