# PeerFS Filesystem Sharing Tool - Node
import time
import peerfs.nodefinder as nodefinder
import peerfs.node
import json
import requests
import keyboard
import threading

f = open("nodes.json", "r")
nodesJson = json.loads(f.read())
nodes = nodesJson["nodes"]
fetchedNodes = []


def fetchAndWriteNodes(ip):
    print(f"[{nodefinder.perf_counter() - nodefinder.start:.5f}] Attempting to fetch nodes from {ip}:18623")
    if ip == peerfs.node.get_ip():
        print(f"[{nodefinder.perf_counter() - nodefinder.start:.5f}] Failed - Own IP")
    try:
        if not ip in fetchedNodes:
            r = requests.get(f"http://{ip}:18623/nodes")
            jsonF = json.loads(r.text)
            for node in jsonF["nodes"]:
                if node not in fetchedNodes:
                    if node not in nodes:
                        fetchedNodes.append(node)
                        nodes.append(node)
                else:
                    print(f"[{nodefinder.perf_counter() - nodefinder.start:.5f}] Node {node} already fetched")
            fetchedNodes.append(ip)
        else:
            print(f"[{nodefinder.perf_counter() - nodefinder.start:.5f}] Node {ip} already fetched")
    except:
        print(f"[{nodefinder.perf_counter() - nodefinder.start:.5f}] Failed to fetch nodes from {ip}")

def nodeFinderDaemon():
    print(f"[{nodefinder.perf_counter() - nodefinder.start:.5f}] NodeFinder daemon started!")
    while True:
        print(f"[{nodefinder.perf_counter() - nodefinder.start:.5f}] Starting NodeFinder, press the \"x\" key within 5 seconds to cancel")
        starttime = nodefinder.perf_counter() - nodefinder.start
        doNodeFinder = True
        while starttime <= 5:
            if keyboard.is_pressed('x'):
                print(f"[{nodefinder.perf_counter() - nodefinder.start:.5f}] Stopping NodeFinder...")
                doNodeFinder = False
                break
            if doNodeFinder:
                executeNodeFinder()

        time.sleep(60)

def executeNodeFinder():   
    for nodeIp in nodefinder.activenodes:
        fetchAndWriteNodes(nodeIp)
    for nodeIp in nodefinder.activenodes:
        if nodeIp not in nodes:
            nodes.append(nodeIp)
    for nodeIp in nodes:
        fetchAndWriteNodes(nodeIp)

def main():
    print(f"[{nodefinder.perf_counter() - nodefinder.start:.5f}] Starting NodeFinder, press the \"x\" key within 5 seconds to cancel or press enter to skip delay...")
    starttime = nodefinder.perf_counter() - nodefinder.start
    curtime = nodefinder.perf_counter() - nodefinder.start
    doNodeFinder = True
    while curtime <= starttime + 5:
        if keyboard.is_pressed('x'):
            print(f"[{nodefinder.perf_counter() - nodefinder.start:.5f}] Stopping NodeFinder...")
            doNodeFinder = False
            break
        elif keyboard.is_pressed('enter'):
            break
        curtime = nodefinder.perf_counter() - nodefinder.start
        
    if doNodeFinder:
        for nodeIp in nodefinder.activenodes:
            fetchAndWriteNodes(nodeIp)
        for nodeIp in nodefinder.activenodes:
            if nodeIp not in nodes:
                nodes.append(nodeIp)
        for nodeIp in nodes:
            fetchAndWriteNodes(nodeIp)


    with open("nodes.json", "w") as f:
        f.write(json.dumps({"nodes": nodes}))
        f.close()
    print(f"[{nodefinder.perf_counter() - nodefinder.start:.5f}] Starting NodeFinder daemon...")
    NodeFinderDaemon = threading.Thread(target=nodeFinderDaemon)
    print(f"[{nodefinder.perf_counter() - nodefinder.start:.5f}] Starting PeerFS Node...")
    peerfs.node.app.run(host=nodefinder.get_ip(), port=18623)


if __name__ == "__main__":
    main()