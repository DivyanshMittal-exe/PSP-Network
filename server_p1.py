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
TCPServerSocket.bind((localIP, server_tcp))    

TCPServerSocket.listen(n)
    
TCPClients = []      
  
while len(TCPClients) < n:
    connectionSocket, addr = TCPServerSocket.accept()
    TCPClients.append(connectionSocket)

print(TCPClients)
        
for index,client in enumerate(TCPClients):
    
    send_chunk_over_TCP(client,index,chunks[index])
    
    chunk_to_send = chunks[index]
    initial_message = str(index) + " " + str(len(chunk_to_send))
    client.send(initial_message.encode())
    
    counter = 0
    while counter < len(chunk_to_send):
        stream_data = chunk_to_send[counter: min(counter + bufferSize,len(chunk_to_send))]
        counter += bufferSize
        client.send(stream_data.encode())
    
    client.send(end_msg.encode())
    

del data
del chunks

UDPServerSockets = [socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) for i in range(n)]
UDPServerSockets = [s.setblocking(False) for s in UDPServerSockets]
UDPServerSockets = [s.bind((localIP,port)) for s,port in zip(UDPServerSockets,udp_server_ports)]

satisfied = [False for i in range(n)]
satisfied_count = 0

while True:
    if satisfied_count == n:
        break
    
    for index,soc,client in enumerate(zip(UDPServerSockets,TCPClients)):
        
        if satisfied[index]:
            continue
        
        try:
            client_req = soc.recvfrom(bufferSize)
            client_req = int(client_req.decode())
            
            if client_req == -1:
                satisfied[index] = True
                satisfied_count += 1
            
            else:
                cache_chunk = cache.get(client_req) 
                
                if cache_chunk == "":
                    bytesToSend   = str.encode(str(client_req))
                    for req_index,req_soc in enumerate(UDPServerSockets):
                        req_soc.sendto(bytesToSend, (localIP, udp_client_ports[req_index]))
                        
                    for index,client in enumerate(TCPClients):
                        server_message = client.recv(bufferSize).decode(errors='ignore')
                        if server_message != "":
                            chunk_index,chunk_len = [int(n) for n in server_message.split()]
                            chunk_data = ""
    
                            counter = 0
                            while True:
                                stream_data = client.recv(bufferSize + 256)
                                # print(stream_data.decode(errors='ignore'))
                                if end_msg in stream_data.decode(errors='ignore'):
                                    chunk_data += stream_data.decode(errors='ignore').replace(end_msg,'')
                                    break
                                chunk_data += stream_data.decode(errors='ignore')
                                counter += bufferSize

                            cache.put(client_req,chunk_data)
                
                cache_chunk = cache.get(client_req) 
                
                initial_message = str(client_req) + " " + str(len(cache_chunk))
                client.send(initial_message.encode())
                
                counter = 0
                while counter < len(cache_chunk):
                    stream_data = cache_chunk[counter: min(counter + bufferSize,len(cache_chunk))]
                    counter += bufferSize
                    client.send(stream_data.encode())
                
                client.send(end_msg.encode())            
        except:
            pass
            
        
        
        


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
    
    



