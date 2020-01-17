#!/bin/bash

SERVICE=AlexaPi

# return YES if running, NO if stopped
systemctl -q is-active AlexaPi  && echo YES || echo NO

systemctl status $SERVICE|grep running	# empty if stopped

# return 0 if running, 1 if stopped !!!
echo $?