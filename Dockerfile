FROM python:3.11-slim-buster

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y postgresql && apt-get clean \
    && pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

ENV DJANGO_SETTINGS_MODULE=aesthetic.settings
ENV PYTHONUNBUFFERED=1

RUN python manage.py migrate

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
