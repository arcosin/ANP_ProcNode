import sys

import PIL
sys.path.append("..")
import argparse
import time
from PIL import Image
from proc_node import Node, buildNodeProcess, TCPNode

NAME_STR = "minimal_example"        # Name of the module. Should use snake case (no spaces).
DESCRIP_STR = "A ProcNode minimal example. Acts like a local echo server."

def main(args):
    node = TCPNode("node-a",True)
    print(node.server.host,node.server.port)
    img = Image.open("test.jpg")
    node.start()
    node.send("node-b",img)

def configCLIParser(parser):
    return parser

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog = NAME_STR, description = DESCRIP_STR)
    parser = configCLIParser(parser)
    args = parser.parse_args()
    main(args)