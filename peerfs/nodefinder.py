from threading import Thread, Lock
from time import perf_counter
from sys import stderr
from time import sleep
import socket, requests

BASE_IP = "192.168.1.%i"
CHECKPORT = 18623
SERVERPORT = 18623
IPS = []
activenodes = []

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

class Threader:
    def __init__(self, threads=30):
        self.thread_lock = Lock()
        self.functions_lock = Lock()
        self.functions = []
        self.threads = []
        self.nthreads = threads
        self.running = True
        self.print_lock = Lock()

    def stop(self) -> None:
        self.running = False

    def append(self, function, *args) -> None:
        self.functions.append((function, args))

    def start(self) -> None:
        for i in range(self.nthreads):
            thread = Thread(target=self.worker, daemon=True)
            thread._args = (thread, )
            self.threads.append(thread)
            thread.start()

    def join(self) -> None:
        for thread in self.threads:
            thread.join()

    def worker(self, thread:Thread) -> None:
        while self.running and (len(self.functions) > 0):
            with self.functions_lock:
                function, args = self.functions.pop(0)
            function(*args)

        with self.thread_lock:
            self.threads.remove(thread)

start = perf_counter()
socket.setdefaulttimeout(0.1)

def connect(hostname, port):
    global IPS
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        result = sock.connect_ex((hostname, port))
    with threader.print_lock:
        if result == 0:
            stderr.write(f"[{perf_counter() - start:.5f}] PeerFS node found at {hostname}\n")
            IPS.append(hostname)

threader = Threader(10)
for i in range(255):
    threader.append(connect, BASE_IP%i, CHECKPORT)
threader.start()
threader.join()
print(f"[{perf_counter() - start:.5f}] Done searching for ips")
for ip in IPS:
    try:
        r = requests.get(f"http://{ip}:{SERVERPORT}/fetchstats")
        print(f"[{perf_counter() - start:.5f}] Found an active node at " + ip + "!")
        activenodes.append(ip)
    except:
        print(f"[{perf_counter() - start:.5f}] {ip} is not running a node.")