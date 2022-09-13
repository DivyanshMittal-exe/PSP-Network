
import numpy as np
from constants import *
import socket
from LRU import  LRU
import sys

import hashlib


data =  []
with open(data_file, 'r') as f:
    while True:
        chunk = f.read(chunkSize)
        
        if not chunk: 
            break
        
        chunk  = chunk.encode('utf-8', errors='ignore').decode('utf-8')
        
        # if len(chunk) < chunkSize:
        #     chunk.ljust(chunkSize)
        
        data.append(chunk)


cache = LRU()

hash = hashlib.md5("".join(data).encode()).hexdigest()

print(hash)

# sys.exit(1)

index_to_split_chunk = np.array_split(np.arange(len(data)), n)

TCP_Clients = []
# TCP_Ports = []

TCPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
TCPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
TCPServerSocket.setsockopt(
        socket.SOL_SOCKET, socket.SO_RCVLOWAT, bufferSize
    )

# TCPServerSocket.setsockopt(
#         socket.SOL_SOCKET, socket.SO_SNDLOWAT, bufferSize
#     )

TCPServerSocket.bind((localIP, server_tcp)) 
TCPServerSocket.listen(n)       




while len(TCP_Clients) < n:

    connectionSocket, addr = TCPServerSocket.accept()
    TCP_Clients.append(connectionSocket)
    
    
    
for index,client in enumerate(TCP_Clients):
    initial_message = str(index).ljust(bufferSize)
    
    client.send(initial_message.encode())
    
    for id in index_to_split_chunk[index]:
        message = (str(id).ljust(chunk_addr_h) + str(len(data[id])).ljust(chunK_len_h) + data[id]).ljust(bufferSize)
        
        client.send(message.encode())
    
    client.send(end_message.encode())
    
del data


UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# UDPServerSocket.settimeout(1)
UDPServerSocket.bind((localIP,server_udp))

satisfied = [False for i in range(n)]
satisfied_count = 0



while True:
    
    
    if all(satisfied):
        break
    
    try:
        client_req = UDPServerSocket.recvfrom(bufferSize)
        print(f"Client asked for {client_req}")
        
        client_index,client_req = [int(i) for i in client_req[0].decode().split()]
        
        if client_req == -1:
            satisfied[client_index] = True
            # satisfied_count += 1

        else:

            if cache.get(client_req)  == "":


                print(f"Initially in cache I dont have {client_req}")

                
                for idf,client_port in enumerate(udp_client_ports):
                    
                    if idf != client_index:
                    
                        # UDPServerSocket.sendto(bytesToSend, (localIP, client_port))
                        # print(f"Sent to {client_port}")
                        message = request_message + " " + str(client_req)
                        
                        print(message)
                        
                        UDPServerSocket.sendto(message.encode(), (localIP, client_port))
                        
                        
                        # TCP_Clients[idf].send(message.encode())
                        
                        client_response = UDPServerSocket.recvfrom(bufferSize)[0].decode()
                        
                        if sending_message in client_response:
                            client_message = getTCPmessage(TCP_Clients[idf])
                        
                        # start_chunk = getTCPmessage(connectionSocket)
                        # client_message = recieve_chunk_over_TCP(server_tcp)
                        
                        
                        # print(client_message)
                        
                        # if client_message != -1 and skip_chunk.strip() not in client_message:
                            if skip_message.strip() not in client_message:
                                chunk_id = int(client_message[:chunk_addr_h])
                                
                                chunk_len = int(client_message[chunk_addr_h:chunk_addr_h + chunK_len_h])
                                
                                chunk = client_message[chunk_addr_h + chunK_len_h: chunk_len + chunk_addr_h + chunK_len_h]
                                
                                cache.put(chunk_id,chunk)
                                break
                    
                    
                # if cache.get(client_req)  == "":
                    
                #     TCPClients[client_index].send(skip_chunk.encode())
                print(f"Trying to get {client_req}")
            
            cache_chunk = cache.get(client_req)
            
            if cache_chunk != "":
            #     TCP_Clients[client_index].send(skip_chunk.encode())
            # else:

                UDPServerSocket.sendto(sending_message.encode(), (localIP, udp_client_ports[client_index]))
            
            
                message = str(client_req).ljust(chunk_addr_h)+ str(len(cache_chunk)).ljust(chunK_len_h) + cache_chunk
                TCP_Clients[client_index].send(message.encode())
                
            # if cache_chunk == "":
            #     print("FF")
            #     # sys.exit(1)
            # else:
            #     message = str(client_req).ljust(header) + cache_chunk
            #     send_chunk_over_TCP(server_tcp,TCP_Ports[client_index],message)
            
            # TCPClients[client_index].send(message.encode())
           
    except Exception as e:
        print(e)
    finally:
        print("Got No request")
        

for client in TCP_Clients:
    client.send(end_message.encode()) 

print(hash)