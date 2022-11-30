FROM python:slim 

WORKDIR /code 

COPY requirements.txt ./
RUN pip install -r requirements.txt 

COPY . .