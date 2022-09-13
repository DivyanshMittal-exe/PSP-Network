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


def make_client(index):
    chunks_not_with_me = [i for i in range(chunk_count)]
    data_with_me = ["" for _ in range(chunk_count)]

    TCPSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    TCPSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # TCPSocket.setsockopt(
    #     socket.SOL_SOCKET, socket.SO_RCVLOWAT, bufferSize
    # )
    
    TCPSocket.bind((localIP, tcp_client_ports[index]))
    TCPSocket.connect((localIP,server_tcp))
    
    # ServerTCP = good_tcp(1,tcp_client_ports[index],server_tcp)
    # ServerUDP = good_udp(udp_client_ports[index])
    UDPSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPSocket.bind((localIP,udp_client_ports[index]))
    
    while True:
        id, chunk = get_chunk(TCPSocket)

        if id == -2:
            break
        
        data_with_me[id] = chunk
        chunks_not_with_me.remove(id)
        
    print(f"Got initial Chunks to {index} {chunk_count - len(chunks_not_with_me)}")
    
    sent_once = False
        
    while True:
        msg_to_send = f"{end_message} {index}"
        if len(chunks_not_with_me)!= 0 :
            req_for = chunks_not_with_me[-1]
            msg_to_send = f"{req_chunk} {req_for} {index}"
            
        if not sent_once:
            print(f"Sending {msg_to_send}")
            send_data(UDPSocket,server_udp_ports[index],msg_to_send)

        if end_message in msg_to_send:
            sent_once = True

        message, id , udp_dat_port= get_data(UDPSocket)
        
        print(f"Got back {message} {id}")
        
        
        if req_chunk in message:
            if id in chunks_not_with_me:
                send_data(UDPSocket,server_udp_ports[udp_dat_port],skip_mesaage)
            else:
                send_data(UDPSocket,server_udp_ports[udp_dat_port],giving_chunk + " 0 " + str(index) )
                send_chunk(TCPSocket,id,data_with_me[id])
                
            
        elif giving_chunk in message:
            print(f"{index} recieving a chunk")
            chunk_id, chunk = get_chunk(TCPSocket, True)      
            print(f"{index} got the {chunk_id} chunk {chunk[:10]} I need {chunks_not_with_me}")
            if chunk != "":
                if chunk_id in chunks_not_with_me:
                    data_with_me[chunk_id] = chunk
                    chunks_not_with_me.remove(chunk_id)
        elif end_message in message:
            break
        elif skip_mesaage in message:
            pass
        else:
            print(f"Yeh konsa packet aagya {message} {id}")
        
        

ts = []

for i in range(n):

    t = threading.Thread(target=make_client,args=[i])
    t.start()
    ts.append(t)
    
for t in ts:
    t.join()

