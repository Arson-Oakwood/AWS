FROM python:3.6.5-alpine
ADD main.py /
ADD dbtest.py /
ADD requirements.txt /
RUN pip install --upgrade pip
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install psycopg2
RUN pip install -r requirements.txt