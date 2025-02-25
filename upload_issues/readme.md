# Upload Issues
Author: Alex Sutay

## Challenge overview
This is sort of a web challenge, but the vulnerability is in cpio so it might be better categorized as misc.
You're given a site where you can view the contents of a cpio archive, as long as you're logged in.
Even better, you can view the flag if you're logged in as admin.
The exploit is that cpio will follow `..` in paths, allowing you to add an administrative user.

## Deployment
This challenge can be run via docker, so deployment should be easy.
First, change the content of `flag.txt` in the main directory from `flag{replace_with_real_flag}` to whatever the flag should be.
Then run `build.sh` to make the zip to provide to participants
To start the challenge, run `docker run -p 8000:8000 --privileged $(docker build -q .)` in the `run` directory
(feel free to change the port as desired).

Provide participants with the source code `archive_investigator.py`, a copy of the `Dockerfile`, and the html templates.
All of them will be bundled into `upload_issues.zip` with a fake flag when you run `build.sh`:
this is what you should provide participants.
Alternatively, you can just provide the `archive_investigator.py` file, it should have evything they need.
However, the Upload Issues 2 challenge will provide the dockerfile, so providing the whole zip gives better parity of the two.
There doesn't need to be any other hints in the description, so feel free to make it whatever you want, or use this one:
"This site lets you look at cpio archives. If only we had an admin account, we could look at the flag..."

This challenge is fairly easy, it's just directory traversal in the cpio command.

## Challenge Details
The auth is simple: there is a directory of json files named with usernames containing passwords and auth levels.
The cpio vuln won't let you overwrite files, but it does let you add, so you just have to include an admin json you know the creds for and you win.
The `solve.sh` script will do every step you need to get the flag.

