FROM python:3.13-slim

WORKDIR /app

RUN pip install Flask

COPY app.py .

VOLUME ["/data"]

EXPOSE 5000

CMD ["python", "app.py"]
