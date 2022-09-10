from constants import *
import socket
import concurrent.futures
import threading

# print(tcp_server_ports)
# print(udp_server_ports)
# print(tcp_client_ports)
# print(udp_client_ports)

def check_port(port):
    with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as s:
        return s.connect_ex((localIP, port)) == 0
    
def make_client(port):
    print(f"{port} {check_port(port)}")
    index = tcp_client_ports.index(port)
    
    chunks_not_with_me = [i for i in range(n)]
    data_with_me = ["" for i in range(n)]
    
    TCPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    TCPClientSocket.bind((localIP, port))
    TCPClientSocket.connect((localIP,server_tcp))
    
    start_chunk = TCPClientSocket.recv(bufferSize).decode(errors='ignore')
    print(start_chunk)    
    chunk_index,chunk_len = [int(n) for n in start_chunk.split()]
    
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
    
    print(f"{index} {port}: {chunk_index} {len(chunk_data)} {chunk_len}")
    
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
