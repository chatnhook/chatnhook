FROM python:2.7-alpine
MAINTAINER "Matjaž Finžgar" <matjaz@finzgar.net>

WORKDIR /app
RUN apk add --update bash && rm -rf /var/cache/apk/*

COPY . /app
COPY bot /app

RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["python", "webhooks.py"]
