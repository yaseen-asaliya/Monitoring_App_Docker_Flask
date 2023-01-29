FROM centos:7.9.2009

RUN yum update -y \
 && yum install -y epel-release \
 && yum install -y python3 python3-pip sysstat crontabs \
 && pip3 install flask \
 && yum clean all

COPY app.py /opt/app.py
COPY statistics_of_usage.py /opt/
COPY statistics_of_usage_module.py /opt/
COPY database_configrations.py /opt/
COPY logger.py /opt/

RUN chmod +x /opt/database_configrations.py \
 && echo "* * * * * /usr/bin/python3 /opt/database_configrations.py" >> /var/spool/cron/root

ENV LC_ALL=en_US.UTF-8

ENTRYPOINT FLASK_APP=/opt/app.py flask run --host=0.0.0.0
