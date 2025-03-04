FROM python:3.9-slim

COPY install_busybox.sh /install_busybox.sh
RUN /install_busybox.sh

WORKDIR /app

RUN pip install flask

COPY archive_investigator.py ./app.py
COPY templates ./templates
COPY flag.txt ./flag.txt
RUN mkdir users && mkdir uploads
CMD ["python", "app.py"]
