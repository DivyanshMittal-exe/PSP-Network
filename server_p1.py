
from re import S
import numpy as np
from constants import *
import socket
from LRU import  LRU
import threading

import random

from socket_func import *


import hashlib



lock = threading.Lock()

data =  []
with open(data_file, 'rb') as f:
    while True:
        chunk = f.read(chunkSize)
        
        if not chunk: 
            break
        
        chunk = chunk.decode('utf-8-sig', errors= 'ignore')
        
        data.append(chunk)



cache = LRU()

hash = hashlib.md5("".join(data).encode()).hexdigest()


print(hash)


oneton = np.arange(len(data))
np.random.shuffle(oneton)
index_to_split_chunk = np.array_split(oneton, n)


is_everyone_done = [False]*n
is_everyone_done_count = 0


TCP_Clients = []

TCPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
TCPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
TCPServerSocket.bind((localIP, server_tcp)) 
TCPServerSocket.listen(n)       


while len(TCP_Clients) < n:

    connectionSocket, addr = TCPServerSocket.accept()
    TCP_Clients.append(connectionSocket)

    
TCP_Clients = sorted(TCP_Clients, key=lambda x: x.getsockname()[1])


print("Hello")

# Server_List = []

# ServerBuffers = [set() for i in range(n)]



class Server:
    # global ServerBuffers
    
    def __init__(self,index):
        
        self.req_buffer = set()
        
        self.TCPSocket = TCP_Clients[index]
        self.UDPSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.UDPSocket.bind((localIP,server_udp_ports[index]))
        self.index = index
        
    
        print(f"Sent initial Chunks to {index}: {len(index_to_split_chunk[index])}")
        
    def add_element_to_list(self,id):
        self.req_buffer.add(id)
    
    def get_init_data(self):
        
        for id in index_to_split_chunk[self.index]:
            send_chunk(self.TCPSocket,id,data[id])
    
        send_chunk(self.TCPSocket,-2,end_message)
        
    
    def handle_load(self):
        global Server_List
        
        global cache
        global is_everyone_done
        global is_everyone_done_count
        global lock

        while True:
            
            if is_everyone_done_count == n:
                send_data(self.UDPSocket,udp_client_ports[self.index],f"{end_message} {self.index}")
                break
                
            req_for = -1
            
            # with lock:
            # print(Server_List)
            print(self.index)
            if len(self.req_buffer) != 0:
                    req_for = self.req_buffer.pop()
            
            if req_for != -1:
                send_data(self.UDPSocket,udp_client_ports[self.index], req_chunk + " " + str(req_for))
                print(f"Asked for {req_for}")

            message, id = get_data(self.UDPSocket)
            
            if skip_mesaage not in message:
                print(f"I got {message} {id}")
            
            if req_chunk in message:
                with lock:
                    cache_message = cache.get(id)
                    
                if cache_message  == "":
                    print(req_chunk + " " + str(id))
            
                    for server in Server_List:
                        
                        if server.index != self.index:
                            # with lock:
                                server.add_element_to_list(id)
                                print(server.req_buffer)
                else:
                    print(f"Able to sen from cache {id} {cache_message[0:10]}")
                    send_data(self.UDPSocket,udp_client_ports[self.index], giving_chunk)
                    send_chunk(self.TCPSocket,id,cache_message)
        
            elif giving_chunk in message:
                with lock:
                    chunk_id, chunk = get_chunk(self.TCPSocket)   
                    print(f"Got chunk {chunk[0:10]}")   
                    if chunk != "":
                            cache.put(chunk_id,chunk)
                    
            elif end_message in message:
            
                print(is_everyone_done)
                
                with lock:
                    if not is_everyone_done[self.index]:
                        is_everyone_done_count += 1
                    is_everyone_done[self.index] = True

            elif skip_mesaage in message:
                pass
            elif exp_message in message:
                print(f" Client {self.index} did nothing ")

            else:
                print(f"Yeh konsa packet aagya {message} {id}")
                
                
        hash = hashlib.md5("".join(data).encode()).hexdigest()
        
        print(hash)
        
    

Server_List = [Server(i) for i in range(n)]    

for server in Server_List:
    server.get_init_data()
        
    
ts = []

for server in Server_List:
    t = threading.Thread(target=server.handle_load(),args=[])
    t.start()
    ts.append(t)
    
for t in ts:
    t.join()
    
    