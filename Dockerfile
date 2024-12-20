# Usar a imagem mais recente do Python
FROM python:3.13-alpine

# Definir o diretório de trabalho dentro do container como /app
WORKDIR /app

RUN apk update && apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    python3-dev \
    build-base \
    mongodb-tools \
    mongodb \
    vim 

# Copiar o arquivo de dependências para o container
COPY requirements.txt .

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt 

# Verificar se o repositório já foi clonado e puxar as últimas atualizações
COPY . /app/

EXPOSE 8000

CMD ["python", "src/manage.py", "runserver","0.0.0.0:8000"]
