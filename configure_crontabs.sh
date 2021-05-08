#!/bin/bash

EMAILS=$1
CRONTAB=$2

# Create the crontab
touch /etc/cron.d/app

# Fill the crontab
echo "$CRONTAB"'    cd /app && .venv/bin/python main.py -m `date +\%-m --date="1 month ago"` -y `date +\%Y --date="1 month ago"` -e '"$EMAILS" >> /etc/cron.d/app

# Give execution rights on the cron job
chmod 0644 /etc/cron.d/app

# Apply cron job
crontab /etc/cron.d/app

# Create the log file to be able to run tail
touch /var/log/cron.log

# Run the cron and show the log
cron && tail -f /var/log/cron.log