from pydoc import cli
from re import T
import numpy as np
from constants import *
import socket
from LRU import  LRU
import sys

data =  []
with open(data_file, 'r') as f:
    while True:
        chunk = f.read(chunkSize)
        
        if not chunk: 
            break
        
        chunk  = chunk.encode('utf-8', errors='ignore').decode('utf-8')
        
        if len(chunk) < 1024:
            chunk.ljust(1024)
        
        data.append(chunk)


cache = LRU()

index_to_split_chunk = np.array_split(np.arange(len(data)), n)

TCPClients = []

TCPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)

TCPServerSocket.setsockopt(
        socket.SOL_SOCKET, socket.SO_RCVLOWAT, bufferSize
    )

# TCPServerSocket.setsockopt(
#         socket.SOL_SOCKET, socket.SO_SNDLOWAT, bufferSize
#     )

TCPServerSocket.bind((localIP, server_tcp)) 
TCPServerSocket.listen(n)       




while len(TCPClients) < n:
    
    connectionSocket, addr = TCPServerSocket.accept()
    TCPClients.append(connectionSocket)
    
    
    
for index,client in enumerate(TCPClients):
    initial_message = str(index).ljust(bufferSize)
    
    client.send(initial_message.encode())
    # print(initial_message)
    
    for id in index_to_split_chunk[index]:
        message = (str(id).ljust(header) + data[id]).ljust(bufferSize)
        client.send(message.encode())
    
    client.send(end_msg.encode())
    
del data

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.setblocking(True)
UDPServerSocket.bind((localIP,server_udp))

satisfied = [False for i in range(n)]
satisfied_count = 0

tcpspill =  ""


while True:
        if satisfied_count == n:
            break
    
    # try:
        client_req = UDPServerSocket.recvfrom(bufferSize)
        print(f"Client asked for {client_req}")
        
        client_index,client_req = [int(i) for i in client_req[0].decode().split()]
        
        if client_req == -1:
            satisfied[client_index] = True
            satisfied_count += 1

        else:
            # cache_chunk = cache.get(client_req) 
            
            
            while cache.get(client_req)  == "":
                print(f"Initially in cache I dont have {client_req}")

                bytesToSend   = str.encode(str(client_req))
                for idf,client_port in enumerate(udp_client_ports):
                    UDPServerSocket.sendto(bytesToSend, (localIP, client_port))
                    client_response = UDPServerSocket.recvfrom(bufferSize)
                    
                    if  client_response == hab:
                    
                        
                        print("Hab")
                        client_message, tcpspill = getTCPmessage(TCPClients[idf])

                        chunk_id = int(client_message[:header])
                        chunk = client_message[header:]
                        cache.put(chunk_id,chunk)
                        
                        break
                    
                    
                if cache.get(client_req)  == "":
                    TCPClients[client_index].send(skip_chunk.encode())
                print(f"Trying to gat {client_req}")
            
            cache_chunk = cache.get(client_req)
            if cache_chunk == "":
                print("FF")
                sys.exit(1)
            
            message = str(client_req).ljust(header) + cache_chunk
            TCPClients[client_index].send(message.encode())
            
    # except:
        # print("Got No request")