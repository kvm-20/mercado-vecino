from fastapi import FastAPI, Response
from pydantic import BaseModel, Field

from app import cache
from app.db import obtener_conexion

app = FastAPI(title="Mercado Vecino API")

CLAVE_TIENDAS = "catalogo:tiendas"


class NuevoPedido(BaseModel):
    tienda_id: int
    cliente: str = Field(min_length=1, max_length=120)
    total: float = Field(gt=0)


@app.get("/health")
def health():
    return {"estado": "ok"}


@app.get("/tiendas")
def listar_tiendas(response: Response):
    # 1) ¿Está en caché? Se responde sin tocar PostgreSQL.
    tiendas = cache.obtener(CLAVE_TIENDAS)
    if tiendas is not None:
        response.headers["X-Cache"] = "HIT"
        return tiendas

    # 2) No está: se consulta la base de datos y se guarda en Redis.
    with obtener_conexion() as conn:
        filas = conn.execute(
            "SELECT id, nombre, barrio FROM tiendas ORDER BY id"
        ).fetchall()
    tiendas = [{"id": f[0], "nombre": f[1], "barrio": f[2]} for f in filas]
    cache.guardar(CLAVE_TIENDAS, tiendas)
    response.headers["X-Cache"] = "MISS"
    return tiendas


@app.get("/pedidos")
def listar_pedidos():
    with obtener_conexion() as conn:
        filas = conn.execute(
            "SELECT id, tienda_id, cliente, total, creado_en FROM pedidos ORDER BY id"
        ).fetchall()
    return [
        {
            "id": f[0],
            "tienda_id": f[1],
            "cliente": f[2],
            "total": float(f[3]),
            "creado_en": f[4].isoformat(),
        }
        for f in filas
    ]


@app.post("/pedidos", status_code=201)
def crear_pedido(pedido: NuevoPedido):
    with obtener_conexion() as conn:
        fila = conn.execute(
            "INSERT INTO pedidos (tienda_id, cliente, total) VALUES (%s, %s, %s) RETURNING id",
            (pedido.tienda_id, pedido.cliente, pedido.total),
        ).fetchone()
    return {"id": fila[0], **pedido.model_dump()}
