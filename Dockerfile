FROM ubuntu:18.04
MAINTAINER Hames "zlewe1997@gmail.com"
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
EXPOSE 80
CMD ["python3","app.py"]
