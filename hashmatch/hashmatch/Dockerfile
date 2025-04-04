# use the jail base image
FROM pwn.red/jail
# copy the root files from any Docker image
COPY --from=ubuntu / /srv
# setup the binary to run
ENV JAIL_TMP_SIZE 255
RUN mkdir /srv/app
copy hashmatch /srv/app/run
copy flag.txt /srv/app/flag.txt
