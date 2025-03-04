# zip the challenge to provide
zip -r upload_issues_2.zip chal
# copy the challenge directory for deployment
rm -r run 2> /dev/null
cp -r chal run
# copy the flag in
cp flag.txt run/flag.txt
