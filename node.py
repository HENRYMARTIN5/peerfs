# A simple flask app that responds to requests with the current node's IP address
from flask import Flask
import platform
import psutil
app = Flask(__name__)

@app.route('/')
def index():
    return "You've located a peerFS node! Good job!"

@app.route('/fetchstats')
def fetchstats():
    # returns the host OS, CPU, and memory usage
    return "Host OS: " + platform.system() + "\n" + "CPU: " + str(psutil.cpu_percent()) + "\n" + "Memory: " + str(psutil.virtual_memory().percent)

if __name__ == '__main__':
    app.run(host=