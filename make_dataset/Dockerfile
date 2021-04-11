FROM python:3.8-slim

USER root

COPY requirements.txt /opt/make_dataset/

RUN pip install -r /opt/make_dataset/requirements.txt && rm /opt/make_dataset/requirements.txt

COPY dataset.py /opt/make_dataset/

WORKDIR /opt/make_dataset
