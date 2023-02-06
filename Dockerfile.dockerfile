FROM python:3.9-slim-buster

# Apache2 package and it's dependencies libapr1 and libaprutil1
# sysstat to run "mpstat" command package
# procps to run "free -m" command package
RUN apt-get update && apt-get -y install apache2 libapr1 libaprutil1 sysstat procps

RUN apt-get update && apt-get -y install python3 python3-pip
RUN pip3 install flask

WORKDIR /app

# set the ServerName directive in Apache's configuration
RUN echo "ServerName localhost" >> /etc/apache2/apache2.conf

# Copy the cron job, Python files, and the HTML file
COPY crontab /etc/cron.d/crontab
COPY *py /app/
COPY /htmls/*.html /var/www/html/

# Give proper permissions to the cron job
RUN chmod 0644 /etc/cron.d/crontab
RUN crontab /etc/cron.d/crontab

# Start Apache2 and the Flask app
ENTRYPOINT service apache2 start && cron && FLASK_APP=/app/app.py flask run --host=0.0.0.0