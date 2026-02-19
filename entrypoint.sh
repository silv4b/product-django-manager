#!/bin/sh
set -e

# Espera o banco estar pronto para não dar erro de conexão recusada
echo "Aguardando banco de dados..."
while ! nc -z postgres14 5432; do
  sleep 0.1
done
echo "Banco de dados online!"

echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

echo "Rodando migrações..."
python manage.py migrate --noinput

echo "Iniciando servidor..."
exec "$@"