#!/bin/sh
# Crea el rol de la aplicación (APP_DB_USER, por defecto mercado_app),
# distinto del superusuario (POSTGRES_USER).
# Principio de mínimo privilegio: solo puede leer y escribir datos en sus
# tablas; no puede crear, borrar ni alterar tablas, ni crear otros roles.
#
# La contraseña se lee del secreto montado en /run/secrets/: nunca está
# escrita en este archivo ni en variables de entorno.
set -eu

APP_PASSWORD="$(cat /run/secrets/db_app_password)"

# Los valores se pasan a psql como variables (-v) y se citan de forma segura
# con :'texto' y :"identificador".
psql -v ON_ERROR_STOP=1 \
     -v app_user="$APP_DB_USER" \
     -v app_password="$APP_PASSWORD" \
     -v db="$POSTGRES_DB" \
     --username "$POSTGRES_USER" \
     --dbname "$POSTGRES_DB" <<'EOSQL'
CREATE ROLE :"app_user" LOGIN PASSWORD :'app_password'
    NOSUPERUSER NOCREATEDB NOCREATEROLE;

-- Nadie más (PUBLIC) se conecta ni crea objetos por defecto
REVOKE ALL ON DATABASE :"db" FROM PUBLIC;
REVOKE CREATE ON SCHEMA public FROM PUBLIC;

-- Permisos justos para la API: solo sobre sus tablas
GRANT CONNECT ON DATABASE :"db" TO :"app_user";
GRANT USAGE ON SCHEMA public TO :"app_user";
GRANT SELECT ON tiendas, productos TO :"app_user";
GRANT SELECT, INSERT ON pedidos TO :"app_user";
GRANT USAGE ON SEQUENCE pedidos_id_seq TO :"app_user";
EOSQL

echo "Rol $APP_DB_USER creado con permisos mínimos"
