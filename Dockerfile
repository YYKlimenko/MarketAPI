FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


WORKDIR /usr/src/backend
COPY ./requirements.txt /usr/src/backend/
RUN pip install -r /usr/src/backend/requirements.txt

COPY . /usr/src/backend



