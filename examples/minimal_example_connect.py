import sys
sys.path.append("..")
import argparse
import time
from proc_node import Node, buildNodeProcess, TCPNode


NAME_STR = "minimal_example"        # Name of the module. Should use snake case (no spaces).
DESCRIP_STR = "A ProcNode minimal example. Acts like a local echo server."




def procBCode(node, _):                                     # Echo process.
    node.start()
    while True:
        msgStr = node.recv()
        if msgStr == "quit":
            node.send("node-a", "Goodbye!")
            break
        else:
            node.send("node-a", "A:  " + msgStr)
    node.stop()


def procACode(node):                                        # User process.
    node.start()
    while True:
        msgStr = input("Send B a message:   ")
        node.send("node-b", msgStr)
        echoStr = node.recv()
        print(echoStr)
        if echoStr == "Goodbye!":
            break
    node.stop()


def main(args):
    #if server is true it will keep waiting for client connection from other node
    nodeA = TCPNode("node-a",False)                        # Create node for process A (this one).
    nodeB = TCPNode("node-b",False)                        # Create node for process B.
    # nodeB.connectTCP(nodeA.id,nodeA.server.host,nodeA.server.port)
    nodeA.connect(nodeB)                          # Connect nodes.
    pb = buildNodeProcess(nodeB, procBCode)       # Make process B with this utility function.
    pb.start()                                    # Start process B.
    time.sleep(0.5)                               # Wait a bit to make sure pb is set up before we start A code.
    procACode(nodeA)                              # Start process A code.
    


def configCLIParser(parser):
    return parser


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog = NAME_STR, description = DESCRIP_STR)
    parser = configCLIParser(parser)
    args = parser.parse_args()
    main(args)

#===============================================================================
