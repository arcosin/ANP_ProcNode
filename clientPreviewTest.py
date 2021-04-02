from client import Client
from server import Server
import cv2

def main():
    host = "192.168.0.102"
    port =  6000
    client = Client(host, port)
    client.start()
    while(True):
        image = client.recv()
        cv2.imshow("Frame",image)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
    client.stop()


    
if __name__ == '__main__':
    main()
        
