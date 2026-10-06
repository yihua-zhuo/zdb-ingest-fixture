import ipaddress
import os
import sqlite3
import socket
import subprocess

from flask import Flask, abort, request

app = Flask(__name__)


@app.route('/ping')
def ping():
    host = request.args.get('host', '')
    try:
        addresses = [ipaddress.ip_address(info[4][0]) for info in
                     socket.getaddrinfo(host, None, type=socket.SOCK_DGRAM)]
    except (OSError, ValueError, UnicodeError):
        abort(400)
    if not addresses or any(not address.is_global or address.is_multicast or
                            address.is_reserved for address in addresses):
        abort(403)
    result = subprocess.run(["ping", "-c", "1", "--", str(addresses[0])], capture_output=True, text=True)
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
    docs_dir = os.path.realpath('docs')
    path = os.path.realpath(os.path.join(docs_dir, name))
    if os.path.commonpath([docs_dir, path]) != docs_dir:
        abort(403)
    with open(path) as fh:
        return fh.read()
