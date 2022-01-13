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
    return "Host OS: " + platform.system() + "\n" + "CPU: " + str(psutil.cpu_percent()) + "%\n" + "Memory: " + str(psutil.virtual_memory().percent) + "%\n" + "Public IP: " + str(psutil.net_if_addrs()['eth0'][0][1])

if __name__ == '__main__':
    app.run(host="192.168.1.115", port=18623)