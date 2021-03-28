import  client , server
 
def main():
    print("start")
    portno =  61619
    name = "Naruto.jpg"
    id = "Server"
    s1 = server.Server( portno , name , id)
    s1.createProxy()
    s1.start()


    
if __name__ == '__main__':
    main()