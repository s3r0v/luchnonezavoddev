
FROM python:latest

RUN mkdir /src
WORKDIR /src
COPY . /src

#RUN apt-get update
#RUN apt-get install -y poppler-utils
RUN pip install -r requirements.txt
