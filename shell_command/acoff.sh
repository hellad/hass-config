#!/bin/bash
irsend SEND_ONCE FUJITSU turn-off                # command to use with alexa and telegram. input select status unchanged yet!!! try to base it on mqtt
echo $(date +%Y:%m:%d) $(date +%H:%M:%S) "irsend SEND_ONCE FUJITSU turn-off was done"  >> /tmp/aircon.log     #it should write to file!
