#!/bin/sh
# Prepara un clon limpio: crea .env a partir de .env.example y genera
# contraseñas aleatorias en secrets/ (ignorada por Git).
# En Windows ejecútelo desde Git Bash o WSL.
set -eu

cd "$(dirname "$0")/.."

[ -f .env ] || cp .env.example .env

mkdir -p secrets
for nombre in db_admin_password db_app_password redis_password; do
  archivo="secrets/$nombre.txt"
  if [ ! -f "$archivo" ]; then
    # hex: sin caracteres especiales que den problemas en URLs o configuraciones
    openssl rand -hex 24 | tr -d "\r\n" > "$archivo"
    echo "Generado $archivo"
  fi
done

# Lectura para los usuarios no root de los contenedores (postgres, redis, app)
chmod 644 secrets/*.txt

echo "Listo. Ahora ejecute: docker compose up -d --build"
