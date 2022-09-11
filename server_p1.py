
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
    # a,p = addr
    # TCP_Ports.append(p)
    
    
    
for index,client in enumerate(TCP_Clients):
    initial_message = str(index).ljust(bufferSize)
    
    client.send(initial_message.encode())
    # print(initial_message)
    
    for id in index_to_split_chunk[index]:
        message = (str(id).ljust(header) + data[id]).ljust(bufferSize)
        client.send(message.encode())
    
    client.send(end_msg.encode())
    
    # client.shutdown(socket.SHUT_RDWR)
    # client.close()

# TCPServerSocket.shutdown(socket.SHUT_RDWR)
# TCPServerSocket.close()

del data

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# UDPServerSocket.setblocking(True)
UDPServerSocket.bind((localIP,server_udp))

satisfied = [False for i in range(n)]
satisfied_count = 0



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
            
            # attempt = 0
            if cache.get(client_req)  == "":
                # attempt += 1
                print(f"Initially in cache I dont have {client_req}")

                bytesToSend   = str.encode(str(client_req))
                for idf,client_port in enumerate(udp_client_ports):
                    
                    
                    UDPServerSocket.sendto(bytesToSend, (localIP, client_port))
                    print(f"Sent to {client_port}")
                    # start_chunk = getTCPmessage(connectionSocket)
                    # client_message = recieve_chunk_over_TCP(server_tcp)
                    client_message = getTCPmessage(TCP_Clients[idf])
                    
                    # print(client_message)
                    
                    # if client_message != -1 and skip_chunk.strip() not in client_message:
                    if skip_chunk.strip() not in client_message:
                        chunk_id = int(client_message[:header])
                        chunk = client_message[header:]
                        cache.put(chunk_id,chunk)
                        break
                    
                    
                # if cache.get(client_req)  == "":
                    
                #     TCPClients[client_index].send(skip_chunk.encode())
                print(f"Trying to get {client_req}")
            
            cache_chunk = cache.get(client_req)
            
            if cache_chunk == "":
                TCP_Clients[client_index].send(skip_chunk.encode())
            else:
                message = str(client_req).ljust(header) + cache_chunk
                TCP_Clients[client_index].send(message.encode())
                
            # if cache_chunk == "":
            #     print("FF")
            #     # sys.exit(1)
            # else:
            #     message = str(client_req).ljust(header) + cache_chunk
            #     send_chunk_over_TCP(server_tcp,TCP_Ports[client_index],message)
            
            # TCPClients[client_index].send(message.encode())
            
    # except:
        # print("Got No request")