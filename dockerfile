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
EXPOSE 8000

ENTRYPOINT ["python", "manage.py", "runserver"]
