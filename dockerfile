FROM python:3.9

RUN mkdir /app
WORKDIR /app

RUN mkdir /app/storage

RUN apt-get update
RUN apt-get install -y git

RUN git clone https://github.com/SweetCase-BakHwa-Project/MicroCloudChip.git

WORKDIR /app/MicroCloudChip
RUN python -m pip install -r requirements.txt
EXPOSE 8000

ENTRYPOINT ["python", "app/manage.py", "runserver"]