FROM python:3.11
WORKDIR /app
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "/app"
COPY ./requirements.txt .
RUN pip install -r requirements.txt
WORKDIR /app/backend
COPY backend .