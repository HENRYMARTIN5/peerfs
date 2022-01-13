# PeerFS Filesystem Sharing Tool - Node
import peerfs.nodefinder as nodefinder
import peerfs.node
import json
import requests

f = open("nodes.json", "r")
nodesJson = json.loads(f.read())
nodes = nodesJson["nodes"]
fetchedNodes = []


def fetchAndWriteNodes(ip):
    print(f"[{nodefinder.perf_counter() - nodefinder.start:.5f}] Attempting to fetch nodes from {ip}:18623")
    if ip == peerfs.node.get_ip():
        print(f"[{nodefinder.perf_counter() - nodefinder.start:.5f}] Failed - Own IP")
        return "Failed. This is the node's ip."
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


def main():
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
    
    print(f"[{nodefinder.perf_counter() - nodefinder.start:.5f}] Starting PeerFS Node...")
    peerfs.node.app.run(host=nodefinder.get_ip(), port=18623)


if __name__ == "__main__":
    main()