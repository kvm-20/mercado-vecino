import os
from pathlib import Path


def leer_secreto(nombre: str) -> str:
    """Busca primero un archivo de secreto (NOMBRE_FILE) y, si no existe,
    la variable de entorno NOMBRE. Si no hay ninguna, la app NO arranca."""
    ruta = os.getenv(f"{nombre}_FILE")
    if ruta and Path(ruta).exists():
        return Path(ruta).read_text().strip()
    valor = os.getenv(nombre)
    if valor is None:
        raise RuntimeError(f"Falta la configuración {nombre}")
    return valor


# PostgreSQL: la API se conecta con el rol de la aplicación (mínimo privilegio),
# nunca con el superusuario.
DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "mercado")
DB_USER = os.getenv("DB_USER", "mercado_app")
DB_PASSWORD = leer_secreto("DB_PASSWORD")

# Redis: caché del catálogo de tiendas
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_PASSWORD = leer_secreto("REDIS_PASSWORD")
CACHE_TTL_SEGUNDOS = int(os.getenv("CACHE_TTL_SEGUNDOS", "60"))
