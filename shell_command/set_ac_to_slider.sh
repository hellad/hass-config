#!/bin/bash
# bash script to change AirConditioner mode in accordance with WEB GUI settings in HASS
# mode transfered as variable

if [ -n "$1" ]
then
echo $(date +%Y:%m:%d) $(date +%H:%M:%S) "irsend SEND_ONCE FUJITSU set2slider  was done  with mode" $1 >> /tmp/aircon.log     #it should write to file!
irsend SEND_ONCE FUJITSU $1
echo $1.
else
echo $(date +%Y:%m:%d) $(date +%H:%M:%S) "No parameters found from set_ac_to_slider "   >> /tmp/aircon.log 
fi

#/usr/bin/irsend SEND_ONCE FUJITSU {mode}

# mode is combination of :
# {{ states.input_select.bedroom_aircon_mode.state }}-{{ states.input_select.bedroom_aircon_fan.state }}-{{ states.input_number.bedroom_aircon_temperature.state|int }}

