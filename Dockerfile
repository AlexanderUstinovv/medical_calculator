FROM python:3.7-alpine

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev git

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /opt/
RUN pip install --upgrade pip
RUN pip install -r /opt/requirements.txt

COPY /app/ /app/

RUN ls /app/

COPY entrypoint.sh /app/

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
