#!/bin/bash
# backup configuration files for HASS 0.88

CONFIG_DIR=/home/homeassistant/.homeassistant
#BACKUP_FILE=/srv/homeassistant/backup/homeassistant_$(date +"%Y%m%d_%H%M").zip
#BACKUP_FILE=/media/yadisk/Software/RaspberryPi/homeassistant/homeassistant_0.64.zip
BACKUP_FILE=/media/yadisk/Software/RaspberryPi/homeassistant/homeassistant_0.88_$(date +"%Y%m%d_%H%M").zip

pushd $CONFIG_DIR >/dev/null
echo
echo "Выполнен переход в каталог `pwd`." # Обратные одиночные кавычки.
echo "На вершине стека находится: $DIRSTACK."

echo
echo "starting back up current system"
zip -9 -q -r $BACKUP_FILE . -x"components/*" -x"deps/*" -x"home-assistant.db" -x"home-assistant_v2.db" -x"home-assistant.log" -x"*.md" -x"*.py"
popd >/dev/null

echo
echo "Возврат в каталог `pwd`."
echo Backup complete: $BACKUP_FILE
