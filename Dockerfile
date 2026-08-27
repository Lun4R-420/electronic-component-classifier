FROM node:20-slim AS frontend-builder

WORKDIR /frontend

COPY frontend/package.json frontend/package-lock.json ./
RUN npm install

COPY frontend/ .
RUN npm run build



FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libxcb1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/
COPY runs/detect/train/weights/best.onnx runs/detect/train/weights/best.onnx
COPY --from=frontend-builder /frontend/dist ./static

EXPOSE 8000

CMD uvicorn src.api:app --host 0.0.0.0 --port ${PORT:-8000}