FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
WORKDIR /app
EXPOSE  5000
CMD ["python3", "/app/src/app.py"]