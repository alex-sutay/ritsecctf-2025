# compile the challenge
gcc -no-pie -fno-stack-protector -o hashmatch/hashmatch hashmatch.c
# zip the challenge to provide to participants
zip -r hashmatch.zip hashmatch
# copy the challenge directory for deployment
rm -r run 2> /dev/null
cp -r hashmatch run
# copy the real flag into the deployment dir
cp flag.txt run/flag.txt
