import socket
import sys
from constants import *

def getTCPmessage(TCPSocket,size_want):
    packet = ""
    len_left = size_want - len(packet)
    
    while len_left != 0:
        message = TCPSocket.recv(len_left).decode('utf-8','ignore')
        packet += message
        len_left = size_want - len(packet)
    
        
    return packet


class good_tcp:
    def __init__(self,type,my_port,connect_port = None):
        
        self.connectionSocket = None
        
        # print("Wow")
        if type == 1:
            

            
            self.TCPSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
            self.TCPSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # self.TCPSocket.setsockopt(
            #     socket.SOL_SOCKET, socket.SO_RCVLOWAT, bufferSize
            # )
            
            self.TCPSocket.bind((localIP, my_port))
            self.TCPSocket.connect((localIP,connect_port))
        else:
            self.TCPSocket = my_port
            self.connectionSocket = connect_port
            # self.TCPSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
            # self.TCPSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # # self.TCPSocket.setsockopt(
            # #         socket.SOL_SOCKET, socket.SO_RCVLOWAT, bufferSize
            # #     )
            # self.TCPSocket.bind((localIP, my_port)) 
            # self.TCPSocket.listen(1)    
            
            # self.connectionSocket, self.addr = self.TCPSocket.accept()
            # self.TCP_Clients = []
            # while len(self.TCP_Clients) < n:
            #     connectionSocket, addr = self.TCPSocket.accept()
            #     self.TCP_Clients.append(connectionSocket)   
            
        # pass
    
    def send_chunk(self,chunk_id , chunk):
        chunk = chunk.encode()
        header_msg = f"{chunk_id} {len(chunk)}"
        message = (header_msg.ljust(headerSize) + chunk)
        if self.connectionSocket:
            self.connectionSocket.send(message.encode())
        else:
            self.TCPSocket.send(message.encode())
    
    def get_chunk(self,blocking = False,time_out = 1):
        sock  = self.TCPSocket
        if self.connectionSocket:
             sock =  self.connectionSocket
        
        sock.setblocking(blocking)
        
        if not blocking:
            sock.settimeout(time_out)
            
        
        chunk = ""
        chunk_id = -1
        
        try:
            initial_header = getTCPmessage(sock,headerSize)
            chunk_id,chunk_len = initial_header.split()
            chunk_id,chunk_len = int(chunk_id),int(chunk_len)
            
            chunk = getTCPmessage(sock,chunk_len)
            # packet = ""
            # len_left = bufferSize - len(packet)    
            # while len_left != 0:
            #     message = sock.recv(len_left).decode('utf-8','ignore')
            #     packet += message
            #     len_left = bufferSize - len(packet)
            
            
            # chunk_id = int(packet[:headerSize])
            # chunk = packet[headerSize:]
            
            return chunk_id,chunk
            
        except socket.timeout:
            print("No packet Recieved, Timed out")
            
                
        except Exception as error:
            print(error)
            sys.exit(1)
            
        finally:
            print("FF Some other error ?")
            
        return chunk_id,chunk