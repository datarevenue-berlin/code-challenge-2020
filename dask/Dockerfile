FROM python:3.6
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

COPY cluster_test.py /root/
COPY requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt
