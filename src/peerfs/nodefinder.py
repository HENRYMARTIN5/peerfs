import requests
from betterlib import ip
import socket
import threading

localMachines = []
baseIp = "192.168.%i.%i"

def connect(hostname, port, logger):
    """
    Check if a machine is running on the given hostname and port.
    """
    global localMachines

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        result = sock.connect_ex((hostname, port))
    if result == 0:
        logger.info("Found local machine at " + hostname)
        localMachines.append(hostname)

def scanLocal(logger):
    """
    Scan the local network for peerfs nodes.
    """
    global localMachines, baseIp

    threads = []

    for i in range(255):
        for j in range(255):
            threads.append(threading.Thread(target=connect, args=(baseIp%(i, j), 18623, logger)))
            threads[-1].start()
    
    for thread in threads:
        thread.join()
    
    return localMachines

def checkIfNode(ips, logger):
    """
    Check if the given IP addresses are running peerfs nodes.
    """

    for ip in ips:
        try:
            r = requests.get("http://" + ip + ":18623/fetchstats", timeout=0.5)
            if r.status_code == 200:
                logger.info("Found peerfs node at " + ip)
                
        except:
            pass