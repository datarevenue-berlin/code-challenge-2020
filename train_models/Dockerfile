FROM python:3.8-slim

USER root

COPY requirements.txt /opt/train_models/

RUN pip install -r /opt/train_models/requirements.txt && rm /opt/train_models/requirements.txt

COPY train_models.py /opt/train_models/

WORKDIR /opt/train_models
