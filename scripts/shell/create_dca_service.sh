#!/usr/bin/env bash

set -e

SERVICE_NAME="dca"
SYSTEMD_PATH="/etc/systemd/system"
SERVICE_FILE="${SYSTEMD_PATH}/${SERVICE_NAME}.service"
POST_DCA_PATH="/path/to/post_dca.py"
VENV_PATH="/path/to/your/venv"
ENV_FILE="/path/to/your/env/file"
USERNAME=$(whoami)

echo "Creating systemd service configuration..."

sudo bash -c "cat > ${SERVICE_FILE}" << EOL
[Unit]
Description=Automated Dollar Cost Averaging Service

[Service]
Type=simple
ExecStart=${VENV_PATH}/bin/python ${POST_DCA_PATH}
Restart=on-failure
User=${USERNAME}
EnvironmentFile=${ENV_FILE}

[Install]
WantedBy=multi-user.target
EOL

echo "Reloading systemd daemon..."
sudo systemctl daemon-reload

echo "Enabling ${SERVICE_NAME} service..."
sudo systemctl enable ${SERVICE_NAME}.service

echo "Starting ${SERVICE_NAME} service..."
sudo systemctl start ${SERVICE_NAME}.service

echo "Checking ${SERVICE_NAME} service status..."
sudo systemctl status ${SERVICE_NAME}.service

echo "Service ${SERVICE_NAME} has been configured and started."
