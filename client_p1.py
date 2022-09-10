from constants import *
import socket
import concurrent.futures
import random
import threading


def make_client(port):
    
    chunks_not_with_me = [i for i in range(n)]
    data_with_me = ["" for i in range(n)]
    
    TCPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    TCPClientSocket.bind((localIP, port))
    TCPClientSocket.connect((localIP,server_tcp))
    
    start_chunk = TCPClientSocket.recv(bufferSize).decode(errors='ignore')
    print(start_chunk)    
    chunk_index,chunk_len = [int(n) for n in start_chunk.split()]
    
    me = chunk_index
    
    chunk_data = ""
    
    counter = 0
    while True:
        stream_data = TCPClientSocket.recv(bufferSize + 256)
        # print(stream_data.decode(errors='ignore'))
        if end_msg in stream_data.decode(errors='ignore'):
            chunk_data += stream_data.decode(errors='ignore').replace(end_msg,'')
            break
        chunk_data += stream_data.decode(errors='ignore')
        counter += bufferSize
    
    # print("Post Counter")
    data_with_me[chunk_index] = chunk_data
    chunks_not_with_me.remove(chunk_index)
    
    print(f"{me} {port}: {chunk_index} {len(chunk_data)} {chunk_len}")
    
    
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPClientSocket.bind((localIP,udp_client_ports[me]))
    
    
    while len(chunks_not_with_me) != 0:
        req_for  = random.choice(chunks_not_with_me)
        bytesToSend   = str.encode(str(req_for))
        
        UDPClientSocket.sendto(bytesToSend, (localIP, udp_server_ports))
        
    
    TCPClientSocket.shutdown(socket.SHUT_RDWR)
    TCPClientSocket.close()

# ts = []

# for port in tcp_client_ports:
#     t = threading.Thread(target=make_client,args=[port])
#     t.start()
#     ts.append(t)
    
# for t in ts:
#     t.join()

with concurrent.futures.ThreadPoolExecutor() as executor:
    # udp_connections = executor.map(make_udp_connection,udp_server_ports)
    tcp_connections = executor.map(make_client,tcp_client_ports)
