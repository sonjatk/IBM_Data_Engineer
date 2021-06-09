# docker build -f sonja.dockerfile -t sonjas-api:latest .

# docker run -p 3000:3000 sonjas-api:latest

FROM python:3.7 AS Build

ENV DEBIANFRONTEND=noninteractive
ENV FLASK_APP=app.py


WORKDIR /opt

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD [ "flask", "run", "-h", "0.0.0.0", "-p", "3000"]
