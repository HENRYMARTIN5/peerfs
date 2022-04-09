------- WORK IN PROGRESS, NO INSTALL INSTRUCTIONS YET -------

PeerFS Idea:
Every client that accesses the Peer to Peer File System will become a node, which will locally cache files, then send them to other peers / clients.

 - Files can be uploaded to your local node, which will send them to other nodes when they view your file.

 - Any node can opt-out of having files cached on their machine.

 - Each file would be assigned a UUID upon uploading, which would be the only way of 
accessing it.

 - When a file is accessed, the UUID is sent to all nodes in the local node’s nodes cache. If any of them have the file cached, it is sent back to the local node. Otherwise, the search will continue through all nodes, going from lowest ping to highest.

 - To build a node cache, the local node would first attempt to ping all local machines / machines in their local network via bruteforce. If no active nodes are found after 35 pings, the local node would resort to fetching a premade node cache from a central server, but only would attempt this once. If no central response could be found, the node would be out of luck.

 - For every node, a random, unused port would be automatically set to internet facing.
 
 - PORT: 18623
