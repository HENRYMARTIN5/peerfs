# PeerFS

## A simple peer-to-peer file sharing system

### Installation

Clone the repo and run the following commands:

```sh
pip install -r requirements.txt
python main.py
```

Wait for it to scan for nodes on your local network. If no nodes are found, then you can add them manually to `nodes.json`.

### Usage

Uploading a file:

The following will perform a ***MASS UPLOAD***. That means that it will upload the file to all nodes in the network. It will take a while to complete, and it will slowly populate the entire network with your file.

```sh
curl \
  --header "id: your-unique-id-here" \ # Replace with your unique ID. If the ID is taken, your request will be ignored.
  --header "filename: your-filename.txt" \ # Replace with the filename you want to upload.
  -F "file=@/your/path/to/file" \ # Upload the file
  http://localhost:18623/requestAddFile/
```

Downloading a file:

```sh
wget http://localhost:18623/file/your-filename.txt # Replace with your filename
```

Viewing all files on a node:

```sh
wget --output-document=filesOnNode.json http://localhost:18623/filestash/
```

Getting all known nodes from another active node:

```sh
wget --output-document=knownNodes.json http://localhost:18623/nodes/
```

Remember, in any of these examples, you can replace `localhost` with any running node's IP or URL.
