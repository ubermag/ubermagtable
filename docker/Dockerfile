FROM ubuntu:18.04

RUN apt-get update -y
RUN apt-get install -y git python3-pip curl
RUN python3 -m pip install --upgrade pip pytest-cov nbval pandas

WORKDIR /usr/local
COPY . /usr/local/ubermagtable/
WORKDIR /usr/local/ubermagtable
RUN python3 -m pip install .
