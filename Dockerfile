FROM python:3.11-alpine

WORKDIR /usr/src/apps/weather_forecast
RUN mkdir -p $WORKDIR/static

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN chmod +x entrypoint.sh
ENTRYPOINT ["/usr/src/apps/weather_forecast/entrypoint.sh"]

CMD python manage.py runserver 0.0.0.0:8000
