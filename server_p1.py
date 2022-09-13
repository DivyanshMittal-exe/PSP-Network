
import numpy as np
from constants import *
import socket
from LRU import  LRU
import threading

from socket_func import *

# from good_tcp import good_tcp

import hashlib

# from good_udp import good_udp



lock = threading.Lock()

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

index_to_split_chunk = np.array_split(np.arange(len(data)), n)

# for i in range()

# ServerTcps = [good_tcp(port) for port in server_tcp_ports]

TCP_Clients = []
# TCP_Ports = []

TCPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
TCPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
TCPServerSocket.bind((localIP, server_tcp)) 
TCPServerSocket.listen(n)       


while len(TCP_Clients) < n:

    connectionSocket, addr = TCPServerSocket.accept()
    TCP_Clients.append(connectionSocket)

print(TCP_Clients[0].getsockname())
    
TCP_Clients = sorted(TCP_Clients, key=lambda x: x.getsockname()[1])
# print()


print("Hello")


def make_server_t(index):
    
    global data
    global cache
    global lock
    
    is_everyone_satisfied = [False for i in range(n)]
    
    print("Hello")
    

    myTCP = TCP_Clients[index]
    UDPSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPSocket.bind((localIP,server_udp_ports[index]))
    # ServerTCP = good_tcp(0,TCPServerSocket,TCP_Clients[i])
    # ServerUDP = good_udp(server_udp_ports[index])
    
    print("Hello")
    
    for id in index_to_split_chunk[index]:
        send_chunk(myTCP,id,data[id])

    
    send_chunk(myTCP,-2,end_message)
    
    print(f"Sent initial Chunks to {index}: {len(index_to_split_chunk[index])}")

    
    while True:    
        message, id , udp_data_port = get_data(UDPSocket)
        print(f"I got {message} {id}")
        

        if req_chunk in message:
            with lock:
                cache_message = cache.get(id)
                if cache_message  == "":
                    for udp_port in udp_client_ports:
                        print(req_chunk + " " + str(id))
                        send_data(UDPSocket,udp_port, req_chunk + " " + str(id) + " " + str(index))
                        message, id , port_with_data = get_data(UDPSocket)

                        if giving_chunk in message:
                            chunk_id, chunk = get_chunk(TCP_Clients[port_with_data])      
                            if chunk != "":
                                cache.put(chunk_id,chunk)

                                send_data(UDPSocket,udp_port, giving_chunk)
                                send_chunk(myTCP,chunk_id,chunk)
                            
                else:
                    send_data(UDPSocket,udp_port, giving_chunk)
                    send_chunk(myTCP,id,cache_message)
            
            # with lock:
            #     cache_message = cache.get(id)
            #     if cache_message  != "":
            #         print(f"Able to Send {id} {cache_message[0:10]}")
            #         send_data(UDPSocket,udp_port, giving_chunk)
            #         send_chunk(myTCP,id,cache_message)
            
        elif giving_chunk in message:
            with lock:
                chunk_id, chunk = get_chunk(TCP_Clients[udp_data_port])      
                if chunk != "":
                        cache.put(chunk_id,chunk)
        elif end_message in message:
            is_everyone_satisfied[id] = True
            if all(is_everyone_satisfied):
                send_data(UDPSocket,udp_client_ports[index],f"{end_message} {index}")
                break
        elif skip_mesaage in message:
            pass
        else:
            print(f"Yeh konsa packet aagya {message} {id}")
    
    
ts = []

for i in range(n):
    t = threading.Thread(target=make_server_t,args=[i])
    t.start()
    ts.append(t)
    
for t in ts:
    t.join()