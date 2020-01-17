#!/bin/bash
# backup system configuration files for HASS

CONFIG_DIR=/etc
#BACKUP_FILE=/srv/homeassistant/backup/system_config_$(date +"%Y%m%d_%H%M").zip
BACKUP_FILE=/media/yadisk/Software/RaspberryPi/homeassistant/sysconfigs_088_$(date +"%Y%m%d_%H%M").zip

pushd $CONFIG_DIR >/dev/null
echo
echo "Выполнен переход в каталог `pwd`." # Обратные одиночные кавычки.
echo "На вершине стека находится: $DIRSTACK."

echo
echo "starting back up current system configuration files"
# zip -9  -r $BACKUP_FILE . -x"components/*" -x"deps/*" -x"home-assistant.db" -x"home-assistant_v2.db" -x"home-assistant.log" -x"*.md" -x"*.py"
zip -9 -q -r $BACKUP_FILE /home/pi/.ssh/ /home/pi/.bash_aliases /etc/letsencrypt/ /etc/crontab /etc/systemd/system/hass-configurator.service  /etc/fstab /etc/group /etc/samba /etc/wpa_supplicant/wpa_supplicant.conf /etc/asound.conf /etc/opt/AlexaPi/ /etc/avahi/ /etc/lirc/ /etc/mosquitto/ /etc/pulse/ /etc/samba/ /etc/sudoers.d/ /etc/systemd/
popd >/dev/null

echo
echo "Возврат в каталог `pwd`."
echo Backup complete: $BACKUP_FILE
