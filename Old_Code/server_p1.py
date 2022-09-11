# from http import server
# from re import I
# from time import sleep
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
    



# TCPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
# TCPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# TCPServerSocket.bind((localIP, server_tcp))    
# TCPServerSocket.settimsend_chunk_over_TCPeout(1000)

# TCPServerSocket.listen(n)

# TCPServerSendSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
# TCPServerSendSocket.bind((localIP, server_send_tcp)) 
    
# TCPClients = []   
# TCP_Ports = []   
  
# while len(TCPClients) < n:
#     connectionSocket, addr = TCPServerSocket.accept()
#     # print(addr)
#     TCPClients.append(connectionSocket)
#     a,p = addr
#     TCP_Ports.append(p)

# sleep(10)


# print(TCPClients)

TCP_Ports = tcp_client_ports
        
for index,client in enumerate(TCP_Ports):
    send_chunk_over_TCP(server_tcp,client,index,chunks[index])
    
# for client in TCPClients:
#     client.shutdown(socket.SHUT_RDWR)
#     client.close()
    
# TCPServerSocket.shutdown(socket.SHUT_RDWR)
# TCPServerSocket.close()

print("Sent all Chunks")

del data
del chunks

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# UDPServerSocket.setblocking(False)
UDPServerSocket.bind((localIP,server_udp))


satisfied = [False for i in range(n)]
satisfied_count = 0

while True:
    if satisfied_count == n:
        break
    
    for index,client in enumerate(TCP_Ports):
        
        if satisfied[index]:
            continue
        
        try:
            client_req = UDPServerSocket.recvfrom(bufferSize)
            print(f"Client asked for {client_req}")
            
            client_port,client_req = [int(i) for i in client_req[0].decode().split()]
            
            
            if client_req == -1:
                satisfied[index] = True
                satisfied_count += 1
            
            else:
                cache_chunk = cache.get(client_req) 
                
                
                if cache_chunk == "":
                    print(f"Initially in cache I dont have {client_req}")
                    bytesToSend   = str.encode(str(client_req))
                    for client_port in udp_client_ports:
                        if client_port != udp_client_ports[index]:
                        # print(client_port)
                            UDPServerSocket.sendto(bytesToSend, (localIP, client_port))
                        
                    for tcp_req_client in TCP_Ports:
                        # print(tcp_req_client)
                        if tcp_req_client != TCP_Ports[index]:
                            chunk_index,chunk_data = recieve_chunk_over_TCP(server_tcp,1)
                        
                        
                        if chunk_index != -1:
                            cache_chunk = chunk_data
                            cache.put(chunk_index,chunk_data)
            
                
                # cache_chunk = cache.get(client_req) 
                
                print(f"Now in cache I have {cache_chunk[0:50]}...")

                if cache_chunk == "":
                    print("I recieved an Empty Chunk")
                    raise "Empty Chunk !"
                else:
                    send_chunk_over_TCP(server_tcp,client,client_req,cache_chunk)    
        except:
            print("Got No request")
            
        
        
        



    

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
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
    
    



