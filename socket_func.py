
from constants import *
import sys
import socket

def send_chunk(TCPSocket,chunk_id , chunk):
    message = (str(chunk_id).ljust(headerSize) + chunk).ljust(bufferSize)
    TCPSocket.send(message.encode())


def get_chunk(sock ,blocking = False,time_out = 10):

    
    # sock.setblocking(blocking)
    
    # if not blocking:
    #     sock.settimeout(time_out)
        
    
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
    
    return chunk_id,chunk
        
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
    
    if req_chunk in server_message:
        m, id , port =  server_message.split()
        return m, int(id), int(port)
        
    
    if end_message in server_message:
        m, id =  server_message.split()
        return m, int(id),0

    return server_message,0,0