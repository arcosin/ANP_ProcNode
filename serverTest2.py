import  client , server
 
def main():
    print("start")
    portno =  61619
    name = "Naruto.jpg"
    id = "Server"
    s1 = server.Server( portno , name , id)
    # s2 = server.Server( portno , name , id)
    s1.start()
    s1.createProxy() 
    


    
if __name__ == '__main__':
    main()