
import argparse
import random
import string
from proc_node import Node, connectAll, buildNodeProcess


NAME_STR = "test_local_ipc"        # Name of the module. Should use snake case (no spaces).
DESCRIP_STR = "ProcNode Local IPC Tester. Tests comunication beetween N processes."


def r():
    return random.randint(1, 10)



def nodeWorker(node, argDict):
    letter = argDict["l"]
    node.start()
    filename = letter + ".txt"                                          # File to log to.
    with open(filename, 'w') as f:                                      # Blank the file.
        f.write("\n")
    nodeList = node.listConnectedNodes()                                # A list of node ids for each connected node.
    finishedNodes = {n: False for n in (nodeList + [node.id])}          # A done-table of every connected node including the current node.
    s = letter * r()                                                    # Initial string, containing the worker's letter a random number of times.
    recNum = 0
    for nid in nodeList:                                                # Send the string to each connected node.
        nextNodes = list(set(nodeList) - set([nid]) - set([node.id]))
        instruct = nextNodes + [node.id]                                # A list of nodes to visit ending with this node.
        node.send(nid, (s, instruct))
    while True:                                                         # Entering recv state.
        s, instruct = node.recv()                                       # Node is updated if needed. Then wait for recv.
        if len(s) > 1 and s[0] == "-":                                  # A node has finished.
            finishedNode = s[1:]
            finishedNodes[finishedNode] = True                          # Set node as finished.
            with open(filename, 'a') as f:
                f.write("Node %s signaled done.\n" % str(finishedNode))
            if False not in set(finishedNodes.values()):                # If all nodes finished, exit.
                break
        elif len(instruct) == 0:                                        # A string has returned.
            with open(filename, 'a') as f:                              # Log the string.
                f.write(s + "\n")
            recNum += 1
            if recNum >= len(nodeList):
                finishedNodes[node.id] = True                               # Set curr node as finished.
                with open(filename, 'a') as f:
                    f.write("This node finished.\n")
                for nid in nodeList:                                        # Notify other nodes.
                    node.send(nid, ("-" + node.id, []))
                if False not in set(finishedNodes.values()):                # If all nodes finished, exit.
                    break
        else:                                                           # A string has arrived to be signed.
            nid = instruct[0]                                           # The next node to send to.
            instruct = instruct[1:]                                     # Remove nid from the list.
            s = s + (letter * r())                                      # Sign string.
            node.send(nid, (s, instruct))                               # Send string on.
    node.stop()
    with open(filename, 'a') as f:
        f.write("Done.\n")



def main(args):
    if args.n >= 2 and args.n < len(string.ascii_letters):
        print("Running simulation with %d nodes.\n" % args.n)
    else:
        print("Error: simulation cannot be run with %d nodes.\n" % args.n)
        return
    mainNode = Node("N-" + string.ascii_letters[0])
    procs = []
    nodes = []
    i = 1
    while i < args.n:
        node = Node("N-" + string.ascii_letters[i])
        nodes.append(node)
        procs.append(buildNodeProcess(node, nodeWorker, argDict = {"l": string.ascii_letters[i]}))
        i += 1
    connectAll(nodes + [mainNode])
    for pr in procs:
        pr.start()
    nodeWorker(mainNode, {"l": string.ascii_letters[i]})





def configCLIParser(parser):
    parser.add_argument("n", nargs = '?', type = int, default = 4, help = "Number of nodes to test with.")
    return parser



if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog = NAME_STR, description = DESCRIP_STR)   # Create module's cli parser.
    parser = configCLIParser(parser)
    args = parser.parse_args()
    main(args)

#===============================================================================
