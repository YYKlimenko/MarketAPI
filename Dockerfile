FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR backend/

COPY requirements.txt backend/marketapi/
RUN pip install -r backend/marketapi/requirements.txt
RUN backend/marketapi/marketapi/manage.py migrate

COPY . backend/marketapi

