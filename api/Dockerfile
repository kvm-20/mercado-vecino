# syntax=docker/dockerfile:1
ARG PYTHON_VERSION=3.13

# ---------- Etapa 1: builder ----------
# Prepara un entorno virtual con las dependencias. Nada más de esta etapa
# llega a la imagen final.
FROM python:${PYTHON_VERSION}-slim AS builder
WORKDIR /build
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
# Primero solo requirements.txt: esta capa queda en caché mientras no cambien
# las dependencias (lo que cambia poco va arriba).
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---------- Etapa 2: test (opcional) ----------
# docker build --target test -t mercado-api:test .
FROM builder AS test
RUN pip install --no-cache-dir pytest httpx
COPY . .
RUN DB_PASSWORD=solo-pruebas REDIS_PASSWORD=solo-pruebas pytest -q

# ---------- Etapa 3: runtime (imagen final) ----------
FROM python:${PYTHON_VERSION}-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"
# Usuario sin privilegios con UID fijo
RUN groupadd --system --gid 10001 app \
 && useradd --system --uid 10001 --gid app --no-create-home app
WORKDIR /app
COPY --from=builder /opt/venv /opt/venv
# El código queda como propiedad de root: el usuario app lo lee, no lo modifica
COPY app/ ./app/
USER app
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1
# Forma exec: Uvicorn recibe SIGTERM y se apaga limpiamente
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
