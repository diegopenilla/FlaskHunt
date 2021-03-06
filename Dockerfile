# Dockerfile - this is a comment. Delete me if you want.
FROM python:3.7-stretch
COPY . /app
WORKDIR /app
RUN pip install --default-timeout=100 -r requirements.txt
ENTRYPOINT ["python"]
CMD ["ZDNA.py"]
