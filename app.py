import os
import sqlite3
import subprocess

from flask import Flask, request

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
    rows = conn.execute(f"SELECT id, name FROM items WHERE name = '{name}'").fetchall()
    return {'items': rows}


@app.route('/file')
def read_file():
    name = request.args.get('name', '')
    with open(os.path.join('docs', name)) as fh:
        return fh.read()
