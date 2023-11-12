# pull official base image
FROM python:3.10-alpine

# set work directory
WORKDIR /usr/src/rzddate

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add gcc python3-dev musl-dev mariadb-dev backports.zoneinfo

# install dependencies
RUN pip install --upgrade pip
ADD ./requirements.txt .
RUN pip install -r requirements.txt

 #copy project
COPY . .
