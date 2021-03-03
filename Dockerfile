FROM python:3.8-slim

# Maintainers
LABEL maintainer="Luckman Ali"

ENV VOLUME 60
ENV FLASK_APP app.py

# Create working directory
RUN mkdir -p /var/automation/

WORKDIR "/var/automation/"

# Install pre-requisites
RUN apt update
RUN apt install cron -y
RUN apt install alsa-utils -y
RUN apt install mplayer -y

# Setup crontab
RUN touch /etc/cron.d/my-cron
RUN chmod 0644 /etc/cron.d/my-cron
RUN crontab /etc/cron.d/my-cron
RUN touch /var/log/cron.log

# Copy code
COPY . .

# Give permissions to files
RUN chmod +x adhan_scheduler/*.py

# Install requirements
RUN pip install .

CMD python ./adhan_scheduler/main.py ${SPEAKER} --volume ${VOLUME} && cron && tail -f /var/log/cron.log
