FROM ruby:2.4.2
RUN apt-get update -yqq 
RUN apt-get install -yqq --no-install-recommends nodejs 
RUN apt-get update && apt-get install -y \
	python3.4 \
	python3-pip
COPY test-interview-question-master /usr/src/app/ 
WORKDIR /usr/src/app 
RUN bundle install 
COPY client.py ./
RUN pip3 install requests