FROM python:3.6-alpine
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

COPY . /opt/orchestrator/

RUN pip install -r /opt/orchestrator/requirements.txt

WORKDIR /opt/orchestrator/
