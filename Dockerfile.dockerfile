FROM python:3.9-slim-buster

# sysstat to run "mpstat" command package
# procps to run "free -m" command package
RUN apt-get update && apt-get -y install cron python3 python3-pip sysstat procps apache2
RUN pip3 install flask requests

WORKDIR /app

COPY crontab /etc/cron.d/crontab
COPY *py /app/
COPY index.html /var/www/html/

RUN chmod 0644 /etc/cron.d/crontab
RUN crontab /etc/cron.d/crontab

ENTRYPOINT cron; FLASK_APP=/app/app.py flask run --host=0.0.0.0; /usr/sbin/apachectl -D FOREGROUND

