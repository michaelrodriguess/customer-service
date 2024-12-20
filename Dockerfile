# Usar uma imagem oficial do Python
FROM python:3.12-alpine

# Definir o diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema necessárias para o projeto
RUN apk update && apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    python3-dev

# Copiar o arquivo de dependências para o contêiner
COPY requirements.txt .

# Instalar as dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código da aplicação para o contêiner
COPY . /app/

# Expor a porta onde o servidor FastAPI vai rodar
EXPOSE 8000

# Comando para rodar o servidor FastAPI com Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
