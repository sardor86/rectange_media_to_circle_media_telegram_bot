# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /rectange_media_to_circle_media_telegram_bot
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN mkdir files
COPY . .
CMD ["python3", "main.py"]
