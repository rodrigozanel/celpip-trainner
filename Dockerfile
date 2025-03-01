# AVISO: ESTE CÓDIGO FOI GERADO POR INTELIGÊNCIA ARTIFICIAL (Claude 3.7 Sonnet)
# NÃO FOI ESCRITO MANUALMENTE PELO AUTOR DO REPOSITÓRIO

FROM python:3.9-slim

WORKDIR /app

# Instalar dependências necessárias para o mysqlclient e ferramentas de diagnóstico
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    pkg-config \
    build-essential \
    curl \
    iputils-ping \
    net-tools \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código da aplicação
COPY . .

# Garantir permissões adequadas
RUN chmod +x docker-entrypoint.sh \
    && mkdir -p /app/app/static/uploads/audio \
    && chmod -R 777 /app/app/static/uploads

# Variáveis de ambiente
ENV FLASK_APP=app
ENV FLASK_ENV=development
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Porta que será exposta
EXPOSE 5000

# Comando para iniciar a aplicação
CMD ["./docker-entrypoint.sh"] 