
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

# for i in range()

# ServerTcps = [good_tcp(port) for port in server_tcp_ports]


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

Server_List = []


class Server:
    
    def __init__(self,index):
        global TCP_Clients
        
        self.TCPSocket = TCP_Clients[index]
        self.request_buffer = []
        self.UDPSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.UDPSocket.bind((localIP,server_udp_ports[index]))
        self.index = index
        for id in index_to_split_chunk[index]:
            send_chunk(self.TCPSocket,id,data[id])
    
        send_chunk(self.TCPSocket,-2,end_message)
    
        print(f"Sent initial Chunks to {index}: {len(index_to_split_chunk[index])}")
        
    
    def handle_load(self):
        global data
        global cache
        global is_everyone_done
        global is_everyone_done_count
        global lock
        
        while True:
            if is_everyone_done_count == n:
                send_data(self.UDPSocket,udp_client_ports[self.index],f"{end_message} {self.index}")
                break
            
            message, id = get_data(self.UDPSocket)
            if skip_mesaage not in message:
                print(f"I got {message} {id}")
            
            if req_chunk in message:
                
                with lock:
                    cache_message = cache.get(id)
                    if cache_message  == "":
                        print(req_chunk + " " + str(id))
                        
                    else:
                        print(f"Able to sen from cache {id} {cache_message[0:10]}")
                        send_chunk(self.TCPSocket,id,cache_message)
                


def make_server_t(index):
    

    
    # is_everyone_satisfied = [False for i in range(n)]
    
    # print("Hello")
    

    myTCP = TCP_Clients[index]


    


    
    while True:    
        
        
        
        
        


        
                

       
            
        elif giving_chunk in message:
            with lock:
                chunk_id, chunk = get_chunk(myTCP)   
                print(f"Got chunk {chunk[0:10]}")   
                if chunk != "":
                        cache.put(chunk_id,chunk)
        elif end_message in message:
            
            print(is_everyone_done)
            
            with lock:
                if not is_everyone_done[index]:
                    is_everyone_done_count += 1
                is_everyone_done[index] = True
                
                
                
        elif skip_mesaage in message:
            if is_everyone_done_count == n:
                print("Sent everyone satisfied")
                send_data(UDPSocket,udp_client_ports[index],f"{end_message} {index}")
                break
        elif exp_message in message:
                print(f" Client {index} did nothing ")
                
                # send_data(UDPSocket,udp_client_ports[index],exp_message)
            # for udp_port in udp_client_ports:
                        
            #     send_data(UDPSocket,udp_port, exp_message)
        else:
            print(f"Yeh konsa packet aagya {message} {id}")
            
    hash = hashlib.md5("".join(data).encode()).hexdigest()

    print(hash)
    
    # print("".join(data))
    
    
ts = []

for i in range(n):
    t = threading.Thread(target=make_server_t,args=[i])
    t.start()
    ts.append(t)
    
for t in ts:
    t.join()
    
    