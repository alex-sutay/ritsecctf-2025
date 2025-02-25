FROM python:3.9-slim

RUN apt update && apt install cpio -y

WORKDIR /app
COPY archive_investigator.py ./app.py
COPY templates ./templates
COPY flag.txt ./flag.txt

RUN pip install flask
RUN useradd flask && chown -R flask:flask /app

USER flask

RUN mkdir users && mkdir uploads
CMD ["python", "app.py"]
