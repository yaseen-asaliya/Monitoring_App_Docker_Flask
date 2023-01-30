FROM python:3.9

RUN apt-get update && apt-get -y install cron vim python3 python3-pip sysstat
RUN pip3 install flask

WORKDIR /opt

COPY crontab /etc/cron.d/crontab

COPY app.py /opt/
COPY statistics_of_usage.py /opt/
COPY statistics_of_usage_module.py /opt/
COPY database_configrations.py /opt/
COPY logger.py /opt/

RUN chmod +x /opt/database_configrations.py

RUN chmod 0644 /etc/cron.d/crontab
RUN /usr/bin/crontab /etc/cron.d/crontab

ENTRYPOINT cron; FLASK_APP=/opt/app.py flask run --host=0.0.0.0
