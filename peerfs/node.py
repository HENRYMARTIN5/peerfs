from flask import Flask, request
import platform
import psutil
import socket
import json
from os import walk
import base64

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

@app.route('/requestAddFile', methods=['PUT'])
def requestAddFile():
    with open("filestash.json", "r") as f:
        filestash = json.loads(f.read())
        if not request.headers.get('filename') in filestash.keys():
            filestash[request.headers.get('filename')] = {"id":request.headers.get('id')}
            with open("filestash.json", "w") as f:
                f.write(json.dumps(filestash))
                f.close()
            f.close()
            with open("./stash/" + request.headers.get('filename'), "wb") as f:
                f.write(base64.decode(request.headers.get('file')))
        else:
            return "File already exists"
    return "File added"

    

if __name__ == '__main__':
    app.run(port=18623)