FROM ubuntu:22.04

WORKDIR /dkb-report

RUN apt-get update -y
RUN apt-get install -y python3 python3-pip
RUN pip install pdfplumber