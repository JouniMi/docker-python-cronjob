FROM python:3.10
RUN apt-get update && apt-get -y install cron vim
WORKDIR /app
COPY crontab /etc/cron.d/crontab
COPY mw_bazaar.py mw_bazaar.py
COPY hybrid.py hybrid.py
COPY triage.py triage.py
RUN chmod 0644 /etc/cron.d/crontab
RUN /usr/bin/crontab /etc/cron.d/crontab
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN echo $PYTHONPATH
# run crond as main process of container
CMD ["cron", "-f"]
