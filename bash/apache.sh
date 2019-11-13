#!/bin/bash
# Author: Arjan de Haan (Vepnar)
# Script to easily move everything to your apache folder

if [ "$(whoami)" != "root" ] ; then
    echo "Execute as root"
    exit
fi

rm -rv /var/www/html
cp -rv ./html /var/www/