#!/bin/bash
echo "Installing cron tasks"
[ -e crontab.txt ] && sudo cp crontab.txt /etc/cron.d/ || echo -n