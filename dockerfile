FROM python:3.12-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .


# Le decimos a Docker que se mueva a la carpeta backend
WORKDIR /app/backend

EXPOSE 8000

# Y ahora arrancamos main:app (sin el "backend." adelante)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]