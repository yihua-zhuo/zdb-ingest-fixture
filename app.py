import os
import sqlite3
import subprocess

from flask import Flask, abort, request

app = Flask(__name__)


@app.route('/ping')
def ping():
    host = request.args.get('host', '')
    result = subprocess.run(["ping", "-c", "1", "--", host], capture_output=True, text=True)
    return result.stdout


@app.route('/item')
def item():
    name = request.args.get('name', '')
    conn = sqlite3.connect('shop.db')
    rows = conn.execute("SELECT id, name FROM items WHERE name = ?", (name,)).fetchall()
    return {'items': rows}


@app.route('/file')
def read_file():
    name = request.args.get('name', '')
    docs_dir = os.path.realpath('docs')
    path = os.path.realpath(os.path.join(docs_dir, name))
    if os.path.commonpath([docs_dir, path]) != docs_dir:
        abort(403)
    with open(path) as fh:
        return fh.read()
