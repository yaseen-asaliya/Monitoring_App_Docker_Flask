FROM python:3.9-slim-buster

# libapr1 and libaprutil1 are dependencies for apache2 package & sysstat to run "mpstat" command & procps to run "free -m" command
RUN apt-get update && apt-get -y install apache2 libapr1 libaprutil1 sysstat procps

RUN apt-get update && apt-get -y install python3 python3-pip
RUN pip3 install flask mysql-connector-python python-dotenv paramiko

WORKDIR /app

# Copy the cron job, Python files, and the HTML file
COPY crontab /etc/cron.d/crontab
COPY *py /app/
COPY /htmls/*.html /var/www/html/
COPY .env /app/

# Give proper permissions to the cron job
RUN chmod 0744 /etc/cron.d/crontab
RUN crontab /etc/cron.d/crontab

# Start Apache2 and the Flask app
ENTRYPOINT service apache2 start && cron && FLASK_APP=/app/app.py flask run --host=0.0.0.0