from constants import *
import socket
import concurrent.futures
import random
import threading


def make_client(port):
    
    chunks_not_with_me = [i for i in range(n)]
    data_with_me = ["" for _ in range(n)]
    
    # TCPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    # TCPClientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # TCPClientSocket.bind((localIP, port))
    # TCPClientSocket.connect((localIP,server_tcp))
    # TCPClientSocket.settimeout(1000)
    
    # TCPClientSocket.settimeout(0)
    
    chunk_index,chunk_data = recieve_chunk_over_TCP(port,None)
    
    
    me = chunk_index
    
    # print("Post Counter")
    data_with_me[chunk_index] = chunk_data
    chunks_not_with_me.remove(chunk_index)
    
    print(f"{me} {port}: {chunk_index} {len(chunk_data)} ")
    
    
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    # UDPClientSocket.setblocking(False)
    UDPClientSocket.bind((localIP,udp_client_ports[me]))
    
    
    while len(chunks_not_with_me) != 0:
        # print("HEre")
        req_for  = random.choice(chunks_not_with_me)
        bytesToSend   = str.encode(str(udp_client_ports[me]) + ' ' + str(req_for))
        
        UDPClientSocket.sendto(bytesToSend, (localIP,server_udp))
        
        try:
            client_req = UDPClientSocket.recvfrom(bufferSize)
            client_req = int(client_req[0].decode())
            print(f"I want {req_for}, I was asked for {client_req} I dont have {chunks_not_with_me}")
            if client_req not in chunks_not_with_me:
                print(f"Sending {data_with_me[client_req][0:10]}")
                send_chunk_over_TCP(port,server_tcp,client_req,data_with_me[client_req])
            else:
                send_ign_over_TCP(port,server_tcp)
        except:
            print("Nothing in UDP Socket")
        

        print(f"{port} Waiting to recieve chunk")
        chunk_index,chunk_data = recieve_chunk_over_TCP(port,5)
        print(f"{port} Got chunk {chunk_index}")
        
        
        # print(chunk_index)
        
        if chunk_index != -1 and chunk_index in chunks_not_with_me:
            chunks_not_with_me.remove(chunk_index)
            print(f"I {port} got {chunk_index}: {chunk_data[0:10]} and left {chunks_not_with_me}")
            
            data_with_me[chunk_index] = chunk_data
        
        
        
    bytesToSend   = str.encode(str(udp_client_ports[me]) + ' ' + str(-1))
    UDPClientSocket.sendto(bytesToSend, (localIP, server_udp))
    
    print("Yes I have all chunks")
        
    
    # TCPClientSocket.shutdown(socket.SHUT_RDWR)
    # TCPClientSocket.close()

ts = []

for port in tcp_client_ports:
    t = threading.Thread(target=make_client,args=[port])
    t.start()
    ts.append(t)
    
for t in ts:
    t.join()

# with concurrent.futures.ThreadPoolExecutor() as executor:
#     # udp_connections = executor.map(make_udp_connection,udp_server_ports)
#     tcp_connections = executor.map(make_client,tcp_client_ports)