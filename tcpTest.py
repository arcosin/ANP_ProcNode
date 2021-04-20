import  client , server , TCPNode , filename


# def main():
#     print("start")
#     portno =  61619 
#     I1 = filename.obj
#     type = "TCP"
#     id = "A"
#     s1 = TCPNode.TCPNode(id , I1, type, portno)
#     s1.serverStart()
#     # s1.recv()


def main():
    print("start")
    portno =  61619 
    I1 = filename.obj
    type = "TCP"
    id = "A"
    s1 = TCPNode.TCPNode(id , I1, type, portno)
    s1.serverStart()
    # s1.serverStart()
    # s1.recv()


if __name__ == '__main__':
    main()