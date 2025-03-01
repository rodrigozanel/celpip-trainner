#!/bin/sh
set -e

echo "============================================"
echo "Iniciando CELPIP Trainer em modo Docker"
echo "============================================"

echo "Verificando configuração..."
# Mostrar as variáveis de ambiente relevantes (sem valores sensíveis)
echo "FLASK_APP: $FLASK_APP"
echo "FLASK_ENV: $FLASK_ENV"
echo "DATABASE URL configurada: $(if [ -n "$DATABASE_URL" ]; then echo "Sim"; else echo "Não"; fi)"

echo "Aguardando o MySQL inicializar..."
# Aguardar mais tempo pelo MySQL
sleep 15

echo "Verificando estrutura de diretórios..."
# Listar diretórios importantes para diagnóstico
ls -la /app
ls -la /app/app
ls -la /app/app/templates

echo "Inicializando o banco de dados..."
python migrations.py

echo "Iniciando a aplicação..."
python run.py 