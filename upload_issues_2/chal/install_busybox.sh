#!/bin/bash

apt update
apt install wget -y


cd /bin
wget https://www.busybox.net/downloads/binaries/1.21.1/busybox-i686 -O busybox
chmod +x busybox

while read -r cmd; do
    if [ -n "$cmd" ]; then
        /bin/busybox rm $cmd 2> /dev/null
        /bin/busybox ln -s /bin/busybox $cmd
    fi
done < <(busybox | sed -e '1,/defined/ d; s/, /\n/g; s/^[ \t]*//; s/,*$//g')
