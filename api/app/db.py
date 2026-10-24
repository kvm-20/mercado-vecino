import psycopg

from app import config


def obtener_conexion() -> psycopg.Connection:
    """Abre una conexión a PostgreSQL con el rol de la aplicación."""
    return psycopg.connect(
        host=config.DB_HOST,
        dbname=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        connect_timeout=5,
    )
