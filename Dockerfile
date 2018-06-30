FROM ubuntu:18.04

RUN apt-get update -y
RUN apt-get install -y git python3-pip curl
RUN python3 -m pip install --upgrade pip pytest-cov nbval \
      pandas openpyxl xlrd xlwt

WORKDIR /usr/local
COPY . /usr/local/oommfodt/
WORKDIR /usr/local/oommfodt
RUN python3 -m pip install .
