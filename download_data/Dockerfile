FROM python:3.6-alpine
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

COPY . /opt/download_data/

RUN pip install -r /opt/download_data/requirements.txt

WORKDIR /opt/download_data/
