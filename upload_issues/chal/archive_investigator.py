from flask import Flask, render_template, session, request, redirect, url_for, abort, flash
from base64 import b64encode
from string import punctuation
import json
import hashlib
import os
import subprocess
import shutil
import random


app = Flask(__name__)
with open('flag.txt', 'rb') as f:
    app.secret_key = f.read()


@app.route('/')
def index():
	return render_template("index.html", user=session.get('user', None))


@app.get('/register')
def get_register():
    return render_template('register.html')

@app.post('/register')
def post_register():
    user = request.form["user"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if None in (user, password1, password2):
        flash('Fill out all fields')
        return redirect(url_for("get_register"))
    for c in punctuation:
        user = user.replace(c, '')
    if len(user) < 1:
        flash('Provide a username')
        return redirect(url_for("get_register"))
    if password1 != password2:
        flash('Passwords must match')
        return redirect(url_for("get_register"))
    if os.path.exists(f'users/{user}.json'):
        flash('User exists')
        return redirect(url_for("get_register"))
    
    d = hashlib.sha256()
    d.update(password1.encode())
    passhash = d.hexdigest()
    user_json = {'passhash': passhash, 'perm_level': 2}

    with open(f'users/{user}.json', 'w') as f:
        json.dump(user_json, f)

    session['perm_level'] = user_json['perm_level']
    session['user'] = user

    return redirect(url_for("index"))


@app.get('/login')
def get_login():
    return render_template('login.html')

@app.post('/login')
def post_login():
    user = request.form["user"]
    password = request.form["password"]
    if None in (user, password):
        flash('Fill out all fields')
        return redirect(url_for("get_login"))
    for c in punctuation:
        user = user.replace(c, '')
    if len(user) < 1:
        flash('Provide a username')
        return redirect(url_for("get_login"))

    if os.path.exists(f'users/{user}.json'):
        with open(f'users/{user}.json') as f:
            user_json = json.loads(f.read())
    else:
        flash('Credential issue')
        return redirect(url_for("get_login"))

            
    d = hashlib.sha256()
    d.update(password.encode())
    passhash = d.hexdigest()
    if passhash != user_json['passhash']:
        flash('Credential issue')
        return redirect(url_for("get_login"))

    session['perm_level'] = user_json['perm_level']
    session['user'] = user

    return redirect(url_for("index"))


@app.route('/logout')
def logout():
    if session.get('perm_level', 1) < 2:
        abort(401)
    del session['perm_level']
    del session['user']
    return 'Logged out!<br><a href="/">return</a>'


@app.get('/archive')
def get_archive():
    if session.get('perm_level', 1) < 2:
        return redirect(url_for('get_login'))
    return render_template('archive_upload.html')

@app.post('/archive')
def post_archive():
    if session.get('perm_level', 1) < 2:
        return redirect(url_for('get_login'))
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('get_archive'))
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('get_archive'))
    if file:
        data = file.read()
        d = hashlib.md5()
        d.update(data)
        d.update(random.randbytes(4))
        tmpname = d.hexdigest()
        os.mkdir(f'uploads/{tmpname}')
        with open(f'uploads/{tmpname}/{tmpname}.cpio', 'wb') as f:
            f.write(data)
        results = subprocess.run([f'cd uploads/{tmpname}/ && cpio -idF {tmpname}.cpio'], shell=True, capture_output=True, text=True)
        if results.returncode != 0:
            shutil.rmtree(f'uploads/{tmpname}')
            flash('A problem occurred with that file: ' + results.stderr)
            return redirect(url_for('get_archive'))
        results = subprocess.run(["find " + f'uploads/{tmpname}' + r" -type f -exec md5sum '{}' \; "], shell=True, capture_output=True, text=True)
        shutil.rmtree(f'uploads/{tmpname}')
        if results.returncode != 0:
            flash('A problem occurred with that file: ' + results.stderr)
            return redirect(url_for('get_archive'))
        rtn = 'MD5 of all files:<br>' + results.stdout.replace(f'uploads/{tmpname}/', '').replace(f'{tmpname}.cpio', file.filename).replace('\n', '<br>')
        return rtn
        
    return redirect(url_for('get_archive'))


@app.route('/admin')
def flag():
    if session.get('perm_level', 1) < 3:
        abort(401)
    return f"For debugging purposes, here is the secret key:\n{b64encode(app.secret_key)}"


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000)
