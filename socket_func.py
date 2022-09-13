
from constants import *
import sys
import socket

def send_chunk(TCPSocket,chunk_id , chunk):
    last_char = chunk[-1]
    last_char = chr(ord(last_char) + 1)
    message = (str(chunk_id).ljust(headerSize) + chunk).ljust(bufferSize, last_char)
    TCPSocket.send(message.encode())


def get_chunk(sock ,blocking = False,time_out = 10):

    try:   
        chunk = ""
        chunk_id = -1
        
        # try:
        packet = ""
        len_left = bufferSize - len(packet)    
        while len_left != 0:
            message = sock.recv(len_left).decode('utf-8','ignore')
            packet += message
            len_left = bufferSize - len(packet)
        
        
        chunk_id = int(packet[:headerSize])
        chunk = packet[headerSize:]
        
        chunk = chunk.rstrip(packet[-1])
        return chunk_id,chunk
    except socket.timeout as e:
        print("TCP Timed OUT")
        return -1,""
    finally:
        sys.exit(1)
    
    
    
        
    # except socket.timeout:
    #     print("No packet Recieved, Timed out")
        
            
    # except Exception as error:
    #     print(error)
    #     sys.exit(1)
        
    # finally:
    #     print("FF Some other error ?")
        
    # return chunk_id,chunk

def send_data(UDPSocket,destination_port,data):
        UDPSocket.sendto(data.encode(), (localIP, destination_port))

def get_data(UDPSocket ,blocking = False,time_out = 1):
    UDPSocket.setblocking(blocking)
    
    if not blocking:
        UDPSocket.settimeout(time_out)
    
    try:
        server_message = UDPSocket.recvfrom(bufferSize)[0].decode()
    except:
        server_message = skip_mesaage
    
    if req_chunk in server_message or end_message in server_message:
        m, id =  server_message.split()
        return m, int(id)

    return server_message,0