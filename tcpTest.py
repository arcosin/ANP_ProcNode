import  client , server , TCPNode , filename

class obbject:
    def __init__(self , attribute):
        self.attribute =  attribute
        self.arr = [0,1,2,3,8,9]


def main():
    print("start")
    portno =  61619 
    I1 = obbject(filename.obj)
    type = "server"
    id = "A"
    s1 = TCPNode.TCPNode(id , I1, type, portno)
    s1.startTCPServer()



    
if __name__ == '__main__':
    main()