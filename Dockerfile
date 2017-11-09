FROM python:2.7-alpine
MAINTAINER "Sander Brand" <brantje@gmail.com>

WORKDIR /app
RUN apk add --update bash && rm -rf /var/cache/apk/*

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 5000
CMD ['ls']

CMD ["python", "/app/captain_hook/endpoint.py"]
