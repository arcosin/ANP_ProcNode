import sys
sys.path.append("..")
from proc_node import TCPNode
import cv2

def main():
    host = "192.168.0.102"
    port =  6000
    client = TCPNode("client", False)
    client.connectTCP("server",host,port)
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
        
