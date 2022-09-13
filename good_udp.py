import socket
import sys
from constants import *




class good_udp:
    def __init__(self,my_port):
        
        self.UDPSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.UDPSocket.bind((localIP,my_port))
        # pass
    
    def send_data(self,destination_port,data):
        self.UDPSocket.sendto(data.encode(), (localIP, destination_port))
       
    
    def get_data(self,blocking = False,time_out = 1):
        self.UDPSocket.setblocking(blocking)
        
        if not blocking:
            self.UDPSocket.settimeout(time_out)
        
        try:
            server_message = self.UDPSocket.recvfrom(bufferSize)[0].decode()
        except:
            server_message = skip_mesaage
        
        if req_chunk in server_message or end_message in server_message:
            m, id =  server_message.split()
            return m, int(id)
    
        return server_message,0