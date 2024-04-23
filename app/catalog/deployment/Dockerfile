FROM python:3.10

WORKDIR /app


ADD ./app/catalog/deployment/requirements.txt /app/app/catalog/deployment/requirements.txt

RUN python3 -m pip install -r /app/app/catalog/deployment/requirements.txt

ADD ./app/catalog /app/app/catalog
ADD ./core /app/core

ENTRYPOINT [ "uvicorn", "app.catalog.main:app" , "--host", "0.0.0.0", "--port", "8081", "--reload"]