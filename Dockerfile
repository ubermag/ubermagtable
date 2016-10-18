FROM ubuntu:16.04

RUN apt-get update -y
RUN apt-get install -y git python3-pip curl
RUN python3 -m pip install --upgrade pip pytest-cov \
      pandas openpyxl xlrd xlwt

WORKDIR /usr/local
RUN git clone https://github.com/joommf/oommfodt.git

WORKDIR /usr/local/oommfodt