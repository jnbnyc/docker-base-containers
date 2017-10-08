FROM python:alpine

RUN apk add --no-cache build-base ca-certificates libffi-dev linux-headers
RUN apk add --no-cache cmake

COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt && rm /app/requirements.txt
COPY main.py /usr/local/src/

WORKDIR /app/
ENTRYPOINT ['python', '/usr/local/src/main.py']
