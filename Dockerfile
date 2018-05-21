FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
RUN apt-get install unzip
RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip 
COPY . /server
WORKDIR /server
RUN pip3 install -r requirements.txt
EXPOSE  5000
WORKDIR /server/app/src/
CMD ["python3", "app.py", "--load", "../../data/fake_profiles.json", "--index", "people"]