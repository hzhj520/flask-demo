from flask import Flask, render_template, redirect, url_for, request, session, abort, flash, make_response
import os
import traceback
from app.util import request_parse, api_result_data, error

from app import app


@app.route('/')
def index():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template("upload.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route('/user/login', methods=['GET', 'POST'])
def login():
    # print("进入login方法---------------------", request.json)
    dict_args = request_parse(request)
    for field in ['username', 'password']:
        if field not in dict_args:
            return error(f"Field {field} is missing!"), 400
    # Get Token
    username = dict_args.get("username")
    password = dict_args.get("password")
    data = {"token": "editor-token"}
    return api_result_data(code=20000, data=data, message="access_token records")

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     error = None
#     if request.method == 'POST':
#         if request.form['username'] != 'admin' or request.form['password'] != 'admin':
#             error = 'Invalid Credentials. Please try again.'
#         else:
#             session['logged_in'] = True
#             flash('Successful login.')
#             return redirect(url_for('index'))
#     return render_template('login.html', error=error)


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect(url_for('index'))


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files['file']
    base_path = "C:\\Users\\E0006294\\work\\temp\\"
    save_path = base_path + file.filename
    current_chunk = int(request.form['dzchunkindex'])
    dzchunkbyteoffset = int(request.form['dzchunkbyteoffset'])
    dztotalfilesize = int(request.form['dztotalfilesize'])

    # If the file already exists it's ok if we are appending to it,
    # but not if it's new file that would overwrite the existing one
    if os.path.exists(save_path) and current_chunk == 0:
        # 400 and 500s will tell dropzone that an error occurred and show an error
        return make_response(('File already exists', 400))

    try:
        with open(save_path, 'ab') as f:
            f.seek(dzchunkbyteoffset)
            f.write(file.stream.read())
    except OSError:
        # log.exception will include the traceback so we can see what's wrong
        print('Could not write to file')
        print(traceback.format_exc())
        return make_response(("Not sure why,"
                              " but we couldn't write the file to disk", 500))

    total_chunks = int(request.form['dztotalchunkcount'])

    if current_chunk + 1 == total_chunks:
        # This was the last chunk, the file should be complete and the size we expect
        if os.path.getsize(save_path) != dztotalfilesize:
            print(f"File {file.filename} was completed, "
                  f"but has a size mismatch."
                  f"Was {os.path.getsize(save_path)} but we"
                  f" expected {dztotalfilesize} ")
            return make_response(('Size mismatch', 500))
        else:
            print(f'File {file.filename} has been uploaded successfully')
    else:
        print(f'Chunk {current_chunk + 1} of {total_chunks} '
              f'for file {file.filename} complete')

    return make_response(("Chunk upload successful", 200))
