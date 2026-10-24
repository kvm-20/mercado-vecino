import json
import logging

import redis

from app import config

log = logging.getLogger("mercado.cache")

# redis-py se conecta de forma perezosa: la conexión real ocurre en el primer uso.
_cliente = redis.Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    password=config.REDIS_PASSWORD,
    socket_timeout=2,
    decode_responses=True,
)


def obtener(clave: str):
    """Devuelve el valor guardado en caché o None. Si Redis falla, la API
    sigue funcionando y consulta directamente la base de datos."""
    try:
        valor = _cliente.get(clave)
        return json.loads(valor) if valor else None
    except redis.RedisError as error:
        log.warning("Redis no disponible al leer %s: %s", clave, error)
        return None


def guardar(clave: str, valor) -> None:
    try:
        _cliente.set(clave, json.dumps(valor), ex=config.CACHE_TTL_SEGUNDOS)
    except redis.RedisError as error:
        log.warning("Redis no disponible al guardar %s: %s", clave, error)
