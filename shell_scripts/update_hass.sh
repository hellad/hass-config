#!/bin/bash

#### script for home-assistant upgrade    ####

# Path variables
#HASS_SERVICE=${HASS_SERVICE:-homeassistant}
HASS_SERVICE=${HASS_SERVICE:-home-assistant@homeassistant.service}
HASS_CONFIG=${HASS_CONFIG:-/home/homeassistant/.homeassistant}
VIRTUAL_ENV=${VIRTUAL_ENV:-/srv/homeassistant}

# This is for log purposes
echo
echo "[$(date)] Update script starting"

# Show package information
$VIRTUAL_ENV/bin/pip3 search homeassistant

# Run the backup script
#$HASS_CONFIG/shell_scripts/backup_config.sh

# Upgrade Home Assistant
echo
echo "Stop Home assistent service"
#sudo systemctl stop home-assistant@homeassistant.service 
sudo systemctl stop "$HASS_SERVICE"

#echo "su as homeassistant and activate venv"
#sudo su -s /bin/bash homeassistant
#source /srv/homeassistant/bin/activate
#$VIRTUAL_ENV/bin/activate

echo
echo "starting upgrade"
$VIRTUAL_ENV/bin/pip3 install --upgrade homeassistant

echo
echo "upgrade finished, not exiting up one level shell"
#exit

# Restart Home Assistant
# This requires a modification using `sudo visudo`:
#   homeassistant ALL=(ALL) NOPASSWD: /bin/systemctl restart home-assistant@homeassistant.service
# Make sure to change `home-assistant.service` to the correct service name
echo
echo "Start Home assistent service: $HASS_SERVICE"
sudo systemctl start "$HASS_SERVICE"

#sudo systemctl start home-assistant@homeassistant.service 

