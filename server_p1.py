from http import server
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

# clients = []

# def make_udp_connection(port):
#     UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
#     UDPServerSocket.bind((localIP,port))
    
# def send_initial_chunk(port):
#     TCPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
#     TCPServerSocket.bind((localIP, port))
#     TCPServerSocket.listen(1)

#     index = tcp_server_ports.index(port)
#     chunk_to_send = chunks[index]
#     # print(f"{port}")
    
    
#     connectionSocket, addr = TCPServerSocket.accept()
    
#     initial_message = str(index) + " " + str(len(chunk_to_send))
    
#     print(f"{connectionSocket} {initial_message}")
#     connectionSocket.send(initial_message.encode())
    
#     counter = 0
#     while counter < len(chunk_to_send):
#         stream_data = chunk_to_send[counter: min(counter + bufferSize,len(chunk_to_send))]
#         counter += bufferSize
#         connectionSocket.send(stream_data.encode())
    
#     connectionSocket.send(end_msg.encode())
    
#     TCPServerSocket.shutdown(socket.SHUT_RDWR)
#     TCPServerSocket.close()



TCPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
TCPServerSocket.bind((localIP, server_tcp))    

TCPServerSocket.listen(n)
    
clients = []      
  
while len(clients) < n:
    connectionSocket, addr = TCPServerSocket.accept()
    clients.append(connectionSocket)

print(clients)
        
for index,client in enumerate(clients):
    chunk_to_send = chunks[index]
    initial_message = str(index) + " " + str(len(chunk_to_send))
    client.send(initial_message.encode())
    
    counter = 0
    while counter < len(chunk_to_send):
        stream_data = chunk_to_send[counter: min(counter + bufferSize,len(chunk_to_send))]
        counter += bufferSize
        client.send(stream_data.encode())
    
    client.send(end_msg.encode())
    


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


# while len(clients) < n:
#     connectionSocket, addr = TCPSockets.accept()
#     chunk_to_send = chunks[len(clients)]
#     connectionSocket.send(str(len(chunk_to_send)).encode())
#     counter = 0
#     while counter < len(chunk_to_send):
#         stream_data = chunk_to_send[counter: min(counter + bufferSize,len(chunk_to_send))]
#         counter += bufferSize
#         connectionSocket.send(stream_data.encode())
    
#     clients.append(connectionSocket)
    
    
del data
del chunks


