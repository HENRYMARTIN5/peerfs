"""
The main entry point for running a peerfs node.
"""

import argparse
from betterlib import logging, config
from time import perf_counter, sleep
import keyboard
from . import nodefinder

# Set start time
start = perf_counter()

# Parse the command line arguments
parser = argparse.ArgumentParser(description='Run a peerfs node.')
parser.add_argument('--nodes', type=str, default='./nodes.json',
                    help='The path to the nodes file.')
parser.add_argument('--stash', type=str, default='./stash', help='The path to the filestash directory.')
parser.add_argument('--logfile', type=str, default='./peerfs-latest.log', help='The log output file.')
args = parser.parse_args()

# Setup logging and open nodes file
logger = logging.Logger(args.logfile, 'peerfs')
nodes = config.ConfigFile(args.nodes)
stashpath = args.stash

def localScan():


def main():
    """
    The main entry point for running a peerfs node.
    """
    global args, logger, nodes, stashpath, start

    # Check if the nodes file is empty
    if nodes.keys() == []:
        logger.info("Found no nodes in nodes file.")
        logger.info("Creating node container...")
        nodes.set("nodes", [])

    logger.info("Starting peerfs node...")

    logger.info("Starting NodeFinder daemon, press the \"x\" key within 3 seconds to cancel...")
    startTime = perf_counter() - start
    while startTime <= 5:
        if keyboard.is_pressed('x'):
            logger.info("Skipping NodeFinder")
            return
    
    logger.info("Beginning local network scan...")


    

    
    



    