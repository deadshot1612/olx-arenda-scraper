FROM python:3.8


RUN apt-get update && apt-get -y install cron vim


WORKDIR /app

COPY crontab /etc/cron.d/crontab
COPY scraper.py /app/scraper.py
ADD scraper.py /
ADD database.py /

RUN chmod 0644 /etc/cron.d/crontab
RUN /usr/bin/crontab /etc/cron.d/crontab

# run crond as main process of container
CMD ["cron", "-f"]