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

server_tcp = 20047
server_send_tcp = server_tcp + 1000

port   = 30050

server_udp = port
port += 1

tcp_client_ports = [i for i in range(port,port + n)]
port += n

udp_client_ports = [i for i in range(port,port + n)]
port += n


def send_chunk_over_TCP(sender_tcp,reciever_tcp,index,chunk_to_send):
    
    TCP_Socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    TCP_Socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    TCP_Socket.bind((localIP, sender_tcp)) 

    TCP_Socket.connect((localIP,reciever_tcp))
    
    initial_message = f"{index} {len(chunk_to_send)}?!?\r\n"
    # str(index) + " " + str(len(chunk_to_send)+ "?!?\r\n")
    TCP_Socket.send(initial_message.encode())
    
    counter = 0
    while counter < len(chunk_to_send):
        stream_data = chunk_to_send[counter: min(counter + bufferSize,len(chunk_to_send))]
        counter += bufferSize
        TCP_Socket.send(stream_data.encode())
    
    TCP_Socket.send(end_msg.encode())
    TCP_Socket.shutdown(socket.SHUT_RDWR)
    TCP_Socket.close()

def send_ign_over_TCP(sender_tcp,reciever_tcp):
    
    TCP_Socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    TCP_Socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    TCP_Socket.bind((localIP, sender_tcp)) 
    TCP_Socket.connect((localIP,reciever_tcp))
    
    TCP_Socket.send(ign_msg.encode())
    TCP_Socket.shutdown(socket.SHUT_RDWR)
    TCP_Socket.close()

def recieve_chunk_over_TCP(reciever_socket,time_out = 1):
    
    TCP_Socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    TCP_Socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    TCP_Socket.bind((localIP, reciever_socket))    
    
    TCP_Socket.listen(1)
    
    # if server_tcp
    if time_out != None:
        TCP_Socket.settimeout(time_out)
    # TCP_Socket.settimeout(time_out)
    start_chunk = ""
    try:
        connectionSocket, addr = TCP_Socket.accept()
        start_chunk = connectionSocket.recv(bufferSize).decode(errors='ignore')
        TCP_Socket.setblocking(1) 
    except:
        pass
    
    
    # TCP_Socket.settimeout(10)
    
    
    if start_chunk == "" or ign_msg in start_chunk:
        # print(start_chunk)
        TCP_Socket.shutdown(socket.SHUT_RDWR)
        TCP_Socket.close()

        return -1,-1
    
    
    chunk_data = ""
    start_chunk = start_chunk.split("?!?\r\n")
    
    if len(start_chunk) == 2:
        chunk_data = start_chunk[1]
    start_chunk = start_chunk[0]
    
    chunk_index,chunk_len = [int(n) for n in start_chunk.split()]
    
    
    counter = 0
    while True:
        stream_data = connectionSocket.recv(bufferSize)
        if end_msg in stream_data.decode(errors='ignore'):
            chunk_data += stream_data.decode(errors='ignore').replace(end_msg,'')
            break
        chunk_data += stream_data.decode(errors='ignore')
        counter += bufferSize
    
    # print(chunk_data[0:100])
    TCP_Socket.shutdown(socket.SHUT_RDWR)
    TCP_Socket.close()
    return (chunk_index,chunk_data)

# tcp_server_ports = generate_ports(n)
# udp_server_ports = generate_ports(n)

# tcp_client_ports = generate_ports(n)
# udp_client_ports = generate_ports(n)


