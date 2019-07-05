# Dockerfile - this is a comment. Delete me if you want.
FROM python:3.7-stretch
COPY . /app
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD gunicorn ZDNA:app -bind 0.0.0.0:$PORT --reload
