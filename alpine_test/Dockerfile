from alpine:3.7

WORKDIR /app

RUN apk add --update python3 && ln -sf /usr/bin/python3.6 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip

RUN pip3 install minio


COPY listdir.py .

# Used soft linke to point python to python3
ENTRYPOINT ["python", "/app/listdir.py"]

