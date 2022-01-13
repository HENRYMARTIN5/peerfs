from flask import Flask
import platform
import psutil
import socket
import json
from os import walk

app = Flask(__name__)

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

@app.route('/')
def index():
    return "peerFS node running on public ip %s" % get_ip()

@app.route('/fetchstats')
def fetchstats():
    # returns the host OS, CPU, and memory usage
    return "Host OS: " + platform.system() + "\n" + "CPU: " + str(psutil.cpu_percent()) + "%\n" + "Memory: " + str(psutil.virtual_memory().percent) + "%\n" + "Public IP: " + get_ip()

@app.route('/nodes')
def nodes():
    with open("nodes.json", "r") as f:
        return f.read()

@app.route('/filestash')
def filestash():
    with open("filestash.json", "r") as f:
        return f.read()

@app.route('/file/<path:filename>')
def file(filename):
    with open("filestash.json", "r") as f:
        filestash = json.loads(f.read())
        if filename in filestash:
            with open("./stash/" + filename, "r") as f:
                return f.read()
        else:
            return "File not found"

if __name__ == '__main__':
    app.run(port=18623)