from this import d
from constants import *
import socket
import concurrent.futures
import random
import threading




    

def make_client(port):
    

    chunks_not_with_me = [i for i in range(chunk_count)]
    data_with_me = ["" for _ in range(chunk_count)]

    TCPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    TCPClientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    TCPClientSocket.setsockopt(
        socket.SOL_SOCKET, socket.SO_RCVLOWAT, bufferSize
    )
    TCPClientSocket.bind((localIP, port))
    TCPClientSocket.connect((localIP,server_tcp))
    



    



    # Get the initial Chunk
    id_message = getTCPmessage(TCPClientSocket)
    # id_message = TCPClientSocket.recv(bufferSize).decode()

    me = int(id_message.strip())
    while True:
        server_message = getTCPmessage(TCPClientSocket)
        # server_message = TCPClientSocket.recv(bufferSize).decode()
        
        if end_msg.strip() in server_message:
            break
        
        chunk_id = int(server_message[:header])
        chunk = server_message[header:]
        
        data_with_me[chunk_id] = chunk
        chunks_not_with_me.remove(chunk_id)
    
    # TCPClientSocket.shutdown(socket.SHUT_RDWR)
    # TCPClientSocket.close()
    
    print(f"{me} recieved first chunk")
    
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    # UDPClientSocket.settimeout(1)
    UDPClientSocket.bind((localIP,udp_client_ports[me]))
    
    
    am_i_satisfied = False
    
    def handle_udp():
        while True:
            if len(chunks_not_with_me) == 0:
                return
            try:
                server_wants = UDPClientSocket.recvfrom(bufferSize)
                server_wants = int(server_wants[0].decode())
                
        
                print(f"{port} want {req_for}, I was asked for {server_wants} I dont have {server_wants in chunks_not_with_me}")
                
                if server_wants not in chunks_not_with_me:
                    print(f"Sending {data_with_me[server_wants][0:10]}")
                    
                    message = str(server_wants).ljust(header) + data_with_me[server_wants]
                        
                    TCPClientSocket.send(message.encode())
                    # send_chunk_over_TCP(port,server_tcp,message)
                    # TCPClientSocket.send(message.encode())
                else:
                    TCPClientSocket.send(skip_chunk.encode())
                    
                    # send_chunk_over_TCP(port,server_tcp,skip_chunk)
                    # UDPClientSocket.sendto(nthab.encode(), (localIP,server_udp))
                    
                    # TCPClientSocket.send(end_msg.encode())
            except Exception as e:
                print(e)
                
            finally:
                print("Nothing in UDP Socket")

    def handle_tcp():
        global chunks_not_with_me
        global data_with_me
        
        while len(chunks_not_with_me) != 0:
            req_for = chunks_not_with_me[-1]
            bytesToSend   = (str(me) + ' ' + str(req_for)).encode()
            
            print(f"Give {me} {req_for}")
            UDPClientSocket.sendto(bytesToSend, (localIP,server_udp))
    
            server_message = getTCPmessage(TCPClientSocket)
            
            if skip_chunk.strip() not in server_message:
                chunk_id = int(server_message[:header])
                chunk = server_message[header:]
                
                data_with_me[chunk_id] = chunk
                chunks_not_with_me.remove(chunk_id)
            
        bytesToSend   = str.encode(str(me) + ' ' + str(-1))
        UDPClientSocket.sendto(bytesToSend, (localIP, server_udp))
        
    
    while len(chunks_not_with_me) != 0:
        req_for = chunks_not_with_me[-1]
        # req_for  = random.choice(chunks_not_with_me)
        bytesToSend   = (str(me) + ' ' + str(req_for)).encode()
        
        print(f"Give {me} {req_for}")
        UDPClientSocket.sendto(bytesToSend, (localIP,server_udp))
        
        try:
            server_wants = UDPClientSocket.recvfrom(bufferSize)
            server_wants = int(server_wants[0].decode())
            print(f"{port} want {req_for}, I was asked for {server_wants} I dont have {server_wants in chunks_not_with_me}")
            if server_wants not in chunks_not_with_me:
                print(f"Sending {data_with_me[server_wants][0:10]}")
                
                message = str(server_wants).ljust(header) + data_with_me[server_wants]
                
               
                # UDPClientSocket.sendto(hab.encode(), (localIP,server_udp))
                
                TCPClientSocket.send(message.encode())
                # send_chunk_over_TCP(port,server_tcp,message)
                # TCPClientSocket.send(message.encode())
            else:
                TCPClientSocket.send(skip_chunk.encode())
                
                # send_chunk_over_TCP(port,server_tcp,skip_chunk)
                # UDPClientSocket.sendto(nthab.encode(), (localIP,server_udp))
                
                # TCPClientSocket.send(end_msg.encode())
        except Exception as e:
            print(e)
            
        finally:
            print("Nothing in UDP Socket")


        # server_message = recieve_chunk_over_TCP(port)
        server_message = getTCPmessage(TCPClientSocket)
        
        # server_message = TCPClientSocket.recv(bufferSize).decode()
        # if server_message != -1:
        if skip_chunk.strip() not in server_message:
            chunk_id = int(server_message[:header])
            chunk = server_message[header:]
            
            data_with_me[chunk_id] = chunk
            chunks_not_with_me.remove(chunk_id)
        


    bytesToSend   = str.encode(str(me) + ' ' + str(-1))
    UDPClientSocket.sendto(bytesToSend, (localIP, server_udp))
    
    print(f"Yes I {port} have all chunks")








ts = []

for port in tcp_client_ports:
    t = threading.Thread(target=make_client,args=[port])
    t.start()
    ts.append(t)
    
for t in ts:
    t.join()