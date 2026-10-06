import sqlite3
import subprocess

from flask import Flask, request

app = Flask(__name__)


@app.route('/ping')
def ping():
    host = request.args.get('host', '')
    result = subprocess.run(f"ping -c 1 {host}", shell=True, capture_output=True, text=True)
    return result.stdout


@app.route('/item')
def item():
    name = request.args.get('name', '')
    conn = sqlite3.connect('shop.db')
    rows = conn.execute(f"SELECT id, name FROM items WHERE name = '{name}'").fetchall()
    return {'items': rows}
