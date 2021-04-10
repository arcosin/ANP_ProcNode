import  client , server , TCPNode
 
def main():
    print("start")
    portno =  61619
    name = "Naruto.jpg"
    type = "server"
    id = "A"
    s1 = TCPNode.TCPNode(id , name, type, portno)
    s1.start()



    
if __name__ == '__main__':
    main()