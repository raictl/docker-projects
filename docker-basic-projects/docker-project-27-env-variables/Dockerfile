FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

ENV APP_NAME="Docker Project 27"
ENV APP_ENV="development"
ENV APP_VERSION="1.0.0"

EXPOSE 5000

CMD ["python", "app.py"]
