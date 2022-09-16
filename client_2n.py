from constants import *
import socket
from LRU import  LRU
import threading
from socket_func import *
import hashlib

import random



lock = threading.Lock()


class Client:
    def __init__(self,index):
        self.index = index
        self.chunks_not_with_me = [i for i in range(chunk_count)]
        self.data_with_me = ["" for _ in range(chunk_count)]
        
        self.TCPSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.TCPSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.TCPSocket.bind((localIP, tcp_client_ports[index]))
        self.TCPSocket.connect((localIP,server_tcp))
        
        self.TCPSocket.settimeout(10)
        
        self.sent_once = False
        
        self.UDPSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.UDPSocket.bind((localIP,udp_client_ports[index]))
        
    def get_init_data(self):
        while True:
            id, chunk = get_chunk(self.TCPSocket)

            if id == -2:
                break
            
            self.data_with_me[id] = chunk
            self.chunks_not_with_me.remove(id)
            
        print(f"Got initial Chunks to {self.index} {chunk_count - len(self.chunks_not_with_me)}")
    
    def client_fetch(self):
            while True:
                
                # pbar.refresh()
                
                msg_to_send = f"{end_message} {self.index}"
            
                if len(self.chunks_not_with_me)!= 0 :
                    # req_for = self.chunks_not_with_me[0]
                    req_for = random.choice(self.chunks_not_with_me[:min(len(self.chunks_not_with_me), n//2)])
                
                    msg_to_send = f"{req_chunk} {req_for}"
                
                if not self.sent_once :
                    send_data(self.UDPSocket,server_udp_ports[self.index],msg_to_send)
                
                    if end_message in msg_to_send:
                        self.sent_once  = True
                        
                chunk_id, chunk = get_chunk(self.TCPSocket, True)      
                
                if chunk_id == -2:
                    break
                elif chunk_id == -1:
                    pass
                elif chunk == "":
                    print("Kuch nhi aaya")
                elif chunk_id in self.chunks_not_with_me:
                    # print(f"Got {chunk_id}: {chunk[:5]}")
                    self.data_with_me[chunk_id] = chunk
                    self.chunks_not_with_me.remove(chunk_id)

    def client_send(self):
        while True:
            message, id = get_data(self.UDPSocket)
            if req_chunk in message:
                if id in self.chunks_not_with_me:
                    send_data(self.UDPSocket,server_udp_ports[self.index],skip_mesaage)
                else:                        
                    send_data(self.UDPSocket,server_udp_ports[self.index],giving_chunk)
                    send_chunk(self.TCPSocket,id,self.data_with_me[id])
             
            elif end_message in message:
                
                    self.TCPSocket.shutdown(socket.SHUT_RDWR)
                    self.TCPSocket.close()           

                    hash = hashlib.md5("".join(self.data_with_me).encode()).hexdigest()
                    print(hash)
                    break
                    
   
clients = [Client(i) for i in range(n)]

for client in clients:             
    client.get_init_data()
    


ts = []

for i,client in enumerate(clients):

    t1 = threading.Thread(target=client.client_fetch,args=[])
    t1.start()
    t2 = threading.Thread(target=client.client_send,args=[])
    t2.start()
    ts.append(t1)
    ts.append(t2)


    
for t in ts:
    t.join()


# def make_client(index):
#     chunks_not_with_me = [i for i in range(chunk_count)]
#     data_with_me = ["" for _ in range(chunk_count)]

#     TCPSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
#     # TCPSocket.settimeout(5)
    
#     TCPSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#     # TCPSocket.setsockopt(
#     #     socket.SOL_SOCKET, socket.SO_RCVLOWAT, bufferSize
#     # )
    
#     # TCPSocket.settimeout(False)
    
#     TCPSocket.bind((localIP, tcp_client_ports[index]))
#     TCPSocket.connect((localIP,server_tcp))
    
#     # ServerTCP = good_tcp(1,tcp_client_ports[index],server_tcp)
#     # ServerUDP = good_udp(udp_client_ports[index])
#     UDPSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
#     UDPSocket.bind((localIP,udp_client_ports[index]))
    
#     while True:
#         id, chunk = get_chunk(TCPSocket)

#         if id == -2:
#             break
        
#         data_with_me[id] = chunk
#         chunks_not_with_me.remove(id)
        
#     print(f"Got initial Chunks to {index} {chunk_count - len(chunks_not_with_me)}")
    
#     sent_once = False
    
    
#     req_for = chunks_not_with_me[0]    
#     msg_to_send = f"{req_chunk} {req_for}"
#     send_data(UDPSocket,server_udp_ports[index],msg_to_send)
    
    
#     while True:


#         message, id = get_data(UDPSocket)
        
#         print(f"Got back {message} {id}")
        
        
#         if req_chunk in message:
#             if id in chunks_not_with_me:
#                 # print(f"{index} don't have {chunks_not_with_me} and I sent skip")
#                 send_data(UDPSocket,server_udp_ports[index],skip_mesaage)
#             else:
#                 # print(f"{index} don't have {chunks_not_with_me} and I sent CHUNK")
                
#                 send_data(UDPSocket,server_udp_ports[index],giving_chunk)
#                 send_chunk(TCPSocket,id,data_with_me[id])
                
            
#         elif giving_chunk in message:
#             # print(f"{index} recieving a chunk")
#             chunk_id, chunk = get_chunk(TCPSocket, True)      
#             # print(f"{index} got the {chunk_id} chunk {chunk[:10]} I need {chunks_not_with_me}")
#             if chunk != "":
#                 if chunk_id in chunks_not_with_me:
#                     data_with_me[chunk_id] = chunk
#                     chunks_not_with_me.remove(chunk_id)
            
            
#             msg_to_send = f"{end_message} {index}"
            
#             if len(chunks_not_with_me)!= 0 :
#                 req_for = chunks_not_with_me[0]
#                 msg_to_send = f"{req_chunk} {req_for}"
                
#             if not sent_once:
#                 # print(f"Sending {msg_to_send}")
#                 if end_message in msg_to_send:
#                     for udp_port in server_udp_ports:
#                         send_data(UDPSocket,udp_port,msg_to_send)
#                         sent_once = True
#                 else:
#                     send_data(UDPSocket,server_udp_ports[index],msg_to_send)
                
            
#         elif end_message in message:
#             break
#         elif skip_mesaage in message:
            

                
#             msg_to_send = f"{end_message} {index}"
            
#             if len(chunks_not_with_me)!= 0 :
#                 req_for = chunks_not_with_me[0]
#                 msg_to_send = f"{req_chunk} {req_for}"
#                 print(f"{msg_to_send}")
                
#             # if not sent_once:
#                 # print(f"Sending {msg_to_send}")
#             # if exp_message in message:
#                 # print(f"Server asked me {index} to do something I send {msg_to_send}")
#                 # print(f"Server asked me {index} to do something I send {msg_to_send} I don't have {chunks_not_with_me}")
                
#             send_data(UDPSocket,server_udp_ports[index],msg_to_send)

#             if end_message in msg_to_send:
#                 for udp_port in server_udp_ports:
#                         send_data(UDPSocket,udp_port,msg_to_send)
#                         sent_once = True
        
#         elif exp_message in message:
            
#             msg_to_send = f"{end_message} {index}"
            
#             if len(chunks_not_with_me)!= 0 :
#                 req_for = random.choice(chunks_not_with_me)
#                 msg_to_send = f"{req_chunk} {req_for}"

#                 print(f"Server asked me {index} to do something I send {msg_to_send}")

#             send_data(UDPSocket,server_udp_ports[index],msg_to_send)

#             if end_message in msg_to_send:
#                 for udp_port in server_udp_ports:
#                         send_data(UDPSocket,udp_port,msg_to_send)
#                         sent_once = True
        
#         else:
#             print(f"Yeh konsa packet aagya {message} {id}")
            
#     # tot = "".join(data_with_me)
#     hash = hashlib.md5("".join(data_with_me).encode()).hexdigest()


#     print(hash)
    
    # print(len(data_with_me))
    # for chunk in data_with_me:
    #     # chunl
    #     print(len(chunk)) 

    
    
        
        



