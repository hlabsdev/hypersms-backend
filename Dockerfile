FROM python:3.9
ENV LANG C.UTF-8

RUN apt-get -y update && apt-get -y autoremove

RUN mkdir /app
WORKDIR /app

RUN apt-get install -y nano

ADD requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt
ADD . /app
RUN python3 manage.py migrate

EXPOSE 8000
EXPOSE 8080
EXPOSE 80
CMD ["gunicorn", "hlabssms.wsgi", "--reload", "-b", "0.0.0.0:8000", "--access-logfile", "-"]

