#!/bin/sh
# This is the script I use to decrypt my second harddrive
# The partitions on my second harddrive (/dev/sda1)
# | 996 GB /dev/arch_home/home | 33GB /dev/arch_home/swap |

if [[ $EUID -ne 0 ]] ; then
   echo "This script must be run as root" 
   exit 1
fi

cryptsetup luksOpen /dev/sda1 arch_home
sleep 3
mkdir -p /home/unknown/gaming
mount /dev/mapper/arch_home-home /home/unknown/gaming
swapon /dev/mapper/arch_home-swap
chown unknown:unknown /home/unknown/gaming