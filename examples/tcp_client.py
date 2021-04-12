import sys
sys.path.append("..")
import argparse
import time
from PIL import Image
from proc_node import Node, buildNodeProcess, TCPNode


NAME_STR = "minimal_example"        # Name of the module. Should use snake case (no spaces).
DESCRIP_STR = "A ProcNode minimal example. Acts like a local echo server."

def procBCode(node, _):                                     # Echo process.
    node.start()
    img = node.recv()
    node.send("node-c", img)
    node.stop()


def procCCode(node):                                        # User process.
    node.start()
    img = node.recv()
    img.show()
    node.stop()


def main(args):
    host = "192.168.55.175"
    port = 33606
    nodeB = TCPNode("node-b",False)
    nodeB.connectTCP("node-a",host,port)
    nodeC = TCPNode("node-c",False)
    nodeB.connect(nodeC)
    pb = buildNodeProcess(nodeB, procBCode)       # Make process B with this utility function.
    pb.start()                                    # Start process B.
    time.sleep(0.5)                               # Wait a bit to make sure pb is set up before we start A code.
    procCCode(nodeC)                              # Start process A code.


def configCLIParser(parser):
    return parser


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog = NAME_STR, description = DESCRIP_STR)
    parser = configCLIParser(parser)
    args = parser.parse_args()
    main(args)