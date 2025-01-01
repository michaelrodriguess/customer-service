FROM python:3.12-alpine

WORKDIR /app

RUN apk update && apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    postgresql-dev \
    python3-dev \
    build-base \
    vim

COPY requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt 

COPY . /app/

EXPOSE 6789

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "6789", "--reload", "--log-config", "configs/log_config.yaml" ]
