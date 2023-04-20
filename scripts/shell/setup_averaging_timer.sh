#!/usr/bin/env bash

set -e

TIMER_NAME="archive_cost_average"
SYSTEMD_PATH="/etc/systemd/system"
TIMER_FILE="${SYSTEMD_PATH}/${TIMER_NAME}.timer"
ENV_FILE="/path/to/your/env/file"

# Load environment variables from .env file

# NOTE: This is not recommended because it pollutes
# the environment and could expose API keys/secrets.
#export $(grep -v '^#' $ENV_FILE | xargs)

# NOTE: This is recommended because it only loads
# the required information into the environment.
FREQUENCY=$(grep '^FREQUENCY=' $ENV_FILE | cut -d '=' -f 2)

# Set FREQUENCY to the value of the environment variable, 
# Defaults to "weekly" if not set
FREQUENCY=${FREQUENCY:-weekly}

echo "Creating systemd timer configuration..."

sudo bash -c "cat > ${TIMER_FILE}" << EOL
[Unit]
Description=Automated Averaging Timer

[Timer]
OnCalendar=${FREQUENCY}
Persistent=true
Unit=archive_average.service

[Install]
WantedBy=timers.target
EOL

echo "Enabling ${TIMER_NAME} timer..."
sudo systemctl enable ${TIMER_NAME}.timer

echo "Starting ${TIMER_NAME} timer..."
sudo systemctl start ${TIMER_NAME}.timer

echo "Checking ${TIMER_NAME} timer status..."
sudo systemctl status ${TIMER_NAME}.timer

echo "Timer ${TIMER_NAME} has been configured and started."
