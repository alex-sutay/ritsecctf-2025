#!/bin/bash

apt update
apt install wget -y


cd /bin
wget https://www.busybox.net/downloads/binaries/1.31.0-i686-uclibc/busybox
chmod +x busybox

while read -r cmd; do
    /bin/busybox rm $cmd 2> /dev/null
    /bin/busybox ln -s /bin/busybox $cmd
done < <(busybox | sed -e '1,/defined/ d; s/, /\n/g; s/^[ \t]*//; s/,*$//g')
