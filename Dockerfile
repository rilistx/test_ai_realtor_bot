FROM python:3.13.7

RUN apt-get update && apt-get upgrade -y

WORKDIR /backend

COPY ./commands ./commands
COPY ./core ./core
COPY ./bot.py ./bot.py
COPY ./alembic.ini ./alembic.ini
COPY ./service_account.json ./service_account.json
COPY ./requirements.txt ./requirements.txt

RUN chmod +x ./commands/*.sh

RUN python3 -m pip install --upgrade pip && \
  pip3 install -r requirements.txt
