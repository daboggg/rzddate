# pull official base image
FROM python:3.10

# set work directory
WORKDIR /usr/src/rzddate

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
ADD ./requirements.txt .
RUN pip install -r requirements.txt

 #copy project
COPY . .
