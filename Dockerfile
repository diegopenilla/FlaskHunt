# Dockerfile - this is a comment. Delete me if you want.
FROM python:3.7-stretch
COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN rm /bin/sh && ln -s /bin/bash /bin/sh
COPY . /app
WORKDIR /app
CMD gunicorn app:app --bind 0.0.0.0:$PORT --reload
