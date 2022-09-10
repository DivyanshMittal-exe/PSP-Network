from http import server
from re import I
import numpy as np
from constants import *
import socket
from LRU import  LRU
import concurrent.futures
import  threading
# print(tcp_server_ports)
# print(udp_server_ports)
# print(tcp_client_ports)
# print(udp_client_ports)

data =  ""
with open(data_file, 'r') as f:
    data = f.read()


index_to_split_chunk = np.array_split(np.arange(len(data)), n)
chunks = [data[x[0]:x[-1] + 1] for x in index_to_split_chunk]
max_chunk_size = max([len(chunk) for chunk in chunks])

cache = LRU(max_chunk_size)

# TCPClients = []

# def make_udp_connection(port):
#     UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
#     UDPServerSocket.bind((localIP,port))
    



TCPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
TCPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
TCPServerSocket.bind((localIP, server_tcp))    
# TCPServerSocket.settimeout(1000)

TCPServerSocket.listen(n)
    
TCPClients = []      
  
while len(TCPClients) < n:
    connectionSocket, addr = TCPServerSocket.accept()
    TCPClients.append(connectionSocket)

print(TCPClients)
        
for index,client in enumerate(TCPClients):
    send_chunk_over_TCP(client,index,chunks[index])
    

print("Sent all Chunks")

del data
del chunks

UDPServerSockets = []
for port in udp_server_ports:
    print(port)
    S = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    S.setblocking(False)
    S.bind((localIP,port))
    UDPServerSockets.append(S)


satisfied = [False for i in range(n)]
satisfied_count = 0

while True:
    if satisfied_count == n:
        break
    
    for index,(soc,client) in enumerate(zip(UDPServerSockets,TCPClients)):
        
        if satisfied[index]:
            continue
        
        try:
            client_req = soc.recvfrom(bufferSize)
            client_req = int(client_req.decode())
            
            print(client_req)
            
            if client_req == -1:
                satisfied[index] = True
                satisfied_count += 1
            
            else:
                cache_chunk = cache.get(client_req) 
                
                if cache_chunk == "":
                    bytesToSend   = str.encode(str(client_req))
                    for req_soc,client_port in zip(UDPServerSockets,udp_client_ports):
                        req_soc.sendto(bytesToSend, (localIP, client_port))
                        
                    for tcp_req_client in TCPClients:
                        chunk_index,chunk_data = recieve_chunk_over_TCP(tcp_req_client)
                        if chunk_index != False:
                            cache.put(chunk_index,chunk_data)
            
                
                cache_chunk = cache.get(client_req) 
                if cache_chunk == "":
                    raise "Empty Chunk !"
                
                send_chunk_over_TCP(client,client_req,cache_chunk)    
        except:
            print("Got No request")
            
        
        
        


TCPServerSocket.shutdown(socket.SHUT_RDWR)
TCPServerSocket.close()
    

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
# ts = []
# for port in tcp_server_ports:
#     t = threading.Thread(target=send_initial_chunk,args=[port])
#     t.start()
#     ts.append(t)
    
# for t in ts:
#     t.join()    


# with concurrent.futures.ThreadPoolExecutor() as executor:
#     # udp_connections = executor.map(make_udp_connection,udp_server_ports)
#     tcp_connections = executor.map(send_initial_chunk,tcp_server_ports)

# TCPSockets = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
# TCPSockets.bind((localIP, Port))
# TCPSockets.listen(n)


# while len(TCPClients) < n:
#     connectionSocket, addr = TCPSockets.accept()
#     chunk_to_send = chunks[len(TCPClients)]
#     connectionSocket.send(str(len(chunk_to_send)).encode())
#     counter = 0
#     while counter < len(chunk_to_send):
#         stream_data = chunk_to_send[counter: min(counter + bufferSize,len(chunk_to_send))]
#         counter += bufferSize
#         connectionSocket.send(stream_data.encode())
    
#     TCPClients.append(connectionSocket)
    
    



