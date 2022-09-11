import socket
import random
from turtle import st
# import re


n = 5
data_file = "A2_small_file.txt"
localIP     = "127.0.0.1"
bufferSize  = 1024
end_msg = "Done_quitting"
ign_msg = "IDontHave"

server_tcp = 20012

port   = 12041

server_udp = port
port += 1

tcp_client_ports = [i for i in range(port,port + n)]
port += n

udp_client_ports = [i for i in range(port,port + n)]
port += n


def send_chunk_over_TCP(TCP_Socket,index,chunk_to_send):
    
    initial_message = f"{index} {len(chunk_to_send)}?!?\r\n"
    # str(index) + " " + str(len(chunk_to_send)+ "?!?\r\n")
    TCP_Socket.send(initial_message.encode())
    
    counter = 0
    while counter < len(chunk_to_send):
        stream_data = chunk_to_send[counter: min(counter + bufferSize,len(chunk_to_send))]
        counter += bufferSize
        TCP_Socket.send(stream_data.encode())
    
    TCP_Socket.send(end_msg.encode())



def recieve_chunk_over_TCP(TCP_Socket):
    TCP_Socket.settimeout(10)
    start_chunk = TCP_Socket.recv(bufferSize).decode(errors='ignore') 
    if start_chunk == "" or ign_msg in start_chunk:
        print(start_chunk)
        return False,False
    
    
    chunk_data = ""
    start_chunk = start_chunk.split("?!?\r\n")
    
    if len(start_chunk) == 2:
        
        chunk_data = start_chunk[1]
    start_chunk = start_chunk[0]
    
    chunk_index,chunk_len = [int(n) for n in start_chunk.split()]
    
    
    counter = 0
    while True:
        stream_data = TCP_Socket.recv(bufferSize + 256)
        if end_msg in stream_data.decode(errors='ignore'):
            chunk_data += stream_data.decode(errors='ignore').replace(end_msg,'')
            break
        chunk_data += stream_data.decode(errors='ignore')
        counter += bufferSize
    
    print(chunk_data[0:100])
    return (chunk_index,chunk_data)

# tcp_server_ports = generate_ports(n)
# udp_server_ports = generate_ports(n)

# tcp_client_ports = generate_ports(n)
# udp_client_ports = generate_ports(n)


