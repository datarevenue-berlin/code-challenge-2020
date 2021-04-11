FROM python:3.8-slim

USER root

RUN apt-get update && apt-get install -y gcc g++

COPY requirements.txt /opt/evaluate/

RUN pip install -r /opt/evaluate/requirements.txt && rm /opt/evaluate/requirements.txt

COPY report.py /opt/evaluate/

WORKDIR /opt/evaluate
