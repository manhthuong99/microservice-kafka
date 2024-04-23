FROM python:3.8

WORKDIR /app


ADD ./app/promotion/deployment/requirements.txt /app/app/promotion/deployment/requirements.txt

RUN python3 -m pip install -r /app/app/promotion/deployment/requirements.txt

ADD ./core /app/core
ADD ./app/promotion /app/app/promotion
ADD ./.env /app/.env


ENTRYPOINT [ "uvicorn", "app.promotion.main:app" , "--host", "0.0.0.0", "--port", "8001", "--reload"]