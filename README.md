# Mercado Vecino — stack contenerizado

Plataforma que conecta tiendas de barrio de Bogotá con sus clientes. Corre en
cuatro contenedores que se levantan con un solo comando:

| Servicio | Imagen | Puerto interno | Red | Función |
|---|---|---|---|---|
| `web` | `mercado-web:1.0` (Nginx sin root) | 8080 (publicado) | frontend | Catálogo y carrito; reenvía `/api` a la API |
| `api` | `mercado-api:1.0` (FastAPI, usuario `app`) | 8000 | frontend + backend | Endpoints `/health`, `/tiendas`, `/pedidos` |
| `db` | `postgres:17-alpine` | 5432 | backend (interna) | Tiendas, productos y pedidos (volumen `pgdata`) |
| `redis` | `redis:7.4-alpine` | 6379 | backend (interna) | Caché del catálogo de tiendas (volumen `redisdata`) |

Solo `web` publica un puerto. La red `backend` es interna: `db` y `redis` no
tienen salida a internet ni son alcanzables desde fuera.

## Requisitos

- Docker Engine 24+ con Compose v2 (`docker compose version`) o Docker Desktop
- Git y `openssl` (en Windows: usar **Git Bash** o WSL)

## Levantar el proyecto desde un clon limpio (4 comandos)

```bash
git clone <URL-del-repositorio> mercado-vecino
cd mercado-vecino
sh scripts/preparar.sh        # crea .env y genera las contraseñas en secrets/
docker compose up -d --build
```

Abrir <http://localhost:8080>.

> En producción se ignora `compose.override.yaml` (recarga en caliente):
> `docker compose -f compose.yaml up -d --build`

## Verificar

```bash
docker compose ps                                   # db, redis y api en (healthy)
curl -i http://localhost:8080/api/tiendas           # 1.ª vez: X-Cache: MISS
curl -i http://localhost:8080/api/tiendas           # 2.ª vez: X-Cache: HIT
docker image ls | grep mercado                      # tamaño de las imágenes
```

## Manejo de credenciales

- Ninguna contraseña está en el código, en los Dockerfiles, en `.env` ni en
  variables de entorno. Viven en `secrets/*.txt` (ignorada por Git) y llegan a
  los contenedores como archivos en `/run/secrets/`.
- `db_admin_password`: superusuario de PostgreSQL, **solo** lo recibe `db`.
- `db_app_password`: rol `mercado_app`, creado en `db/init/02_rol_app.sh` con
  permisos mínimos (`SELECT` en tiendas y productos, `SELECT/INSERT` en pedidos).
- `redis_password`: lo reciben `redis` y `api`.

## Auditoría de credenciales

```bash
git log -p | grep -iE "password|secret|token"
git ls-files | grep -E "\.env$|secrets/"
docker history --no-trunc mercado-api:1.0 | grep -iE "password|token"
docker inspect mercado-vecino-api-1 --format '{{json .Config.Env}}'
```

Los resultados solo deben mostrar nombres de variables (`DB_PASSWORD_FILE`,
`REDIS_PASSWORD_FILE`), nunca valores.

## Ciclo de vida

```bash
docker compose down       # borra contenedores y redes; conserva los datos
docker compose down -v    # borra también los volúmenes: datos perdidos
```

Si cambian las contraseñas en `secrets/`, hay que empezar con `down -v`,
porque PostgreSQL solo crea los usuarios cuando el volumen está vacío.

## Estructura

```
mercado-vecino/
├── api/            # FastAPI + Dockerfile multi-etapa (builder, test, runtime)
├── frontend/       # React + Vite + Dockerfile multi-etapa con Nginx
├── db/init/        # 01_esquema.sql (tablas y semilla), 02_rol_app.sh (rol)
├── scripts/        # preparar.sh
├── compose.yaml
├── compose.override.yaml
└── .env.example
```
