#!/bin/sh

# Espera o banco de dados ficar pronto (opcional mas recomendado)
echo "Rodando migrações..."
python manage.py migrate --noinput

# Inicia o Gunicorn (comando original do seu Dockerfile)
exec "$@"