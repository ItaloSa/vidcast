FROM python:3.8-slim

COPY requirements.txt .

RUN apt update
RUN apt install ffmpeg -y

# install dependencies
RUN pip3 install -r requirements.txt
