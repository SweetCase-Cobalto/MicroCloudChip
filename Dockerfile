FROM python:3.9

RUN mkdir /app
WORKDIR /app

RUN mkdir /app/storage

RUN apt-get update
RUN apt-get install -y git

RUN git clone https://github.com/SweetCase-BakHwa-Project/MicroCloudChip.git

WORKDIR /app/MicroCloudChip
RUN python -m pip install -r requirements.txt

WORKDIR /app/MicroCloudChip/app
RUN sh refresh.sh

ENV PORT 8000
ENV IP 0.0.0.0

ENTRYPOINT ["sh", "-c", "python manage.py runserver $IP:$PORT"]
