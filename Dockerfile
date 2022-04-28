# FROM continuumio/miniconda:latest

FROM python:3.9

WORKDIR /code

COPY requirements.txt .

RUN pip install --upgrade pip 

RUN pip install --no-cache-dir --upgrade -r requirements.txt