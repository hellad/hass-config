#!/bin/bash
echo "running"
touch /config/test.txt;
echo "test" > /config/test.txt;

# https://toster.ru/q/542064
SRC_DIR=/usr/syno/etc/certificate/_archive/VUwgyv   #/path/to/mounted/volume
DIR=/config/certificates                            #/path/to/dir
USER=admin
GROUP=users

$uid=$(stat -c '%u' $SRC_DIR)                                                                                                                    
$gid=$(stat -c '%g' $SRC_DIR)                                                                                                                    
echo $uid > /root/uid                                                                                                                          
echo $gid > /root/gid                                                                                                                          
usermod -u $uid $USER                                                                                                                                   
groupmod -g $gid $GROUP                                                                                                                                  
mkdir -p $DIR                                                                                                                                            
chown -R $USER:$GROUP $DIR