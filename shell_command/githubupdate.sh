#!/bin/bash

#### https://www.home-assistant.io/docs/ecosystem/backup/backup_github/

#ls /volume1/docker/homeassistant/config
#pause

cd /volume1/docker/homeassistant/config/

git add .
git status
echo -n "Enter the Description for the Change: " [Minor Update]
read CHANGE_MSG
git commit -m "${CHANGE_MSG}"
git push origin master

exit