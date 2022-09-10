import socket
import random



n = 5
data_file = "A2_small_file.txt"
localIP     = "127.0.0.1"
bufferSize  = 1024
end_msg = "Done_quitting"

server_tcp = 20000

port   = 20220 
tcp_client_ports = [i for i in range(port,port + n)]
port += n

udp_server_ports = [i for i in range(port,port + n)]
port += n

udp_client_ports = [i for i in range(port,port + n)]
port += n


def send_chunk_over_TCP(TCP_Socket,index,chunk_to_send):
    
    initial_message = str(index) + " " + str(len(chunk_to_send))
    TCP_Socket.send(initial_message.encode())
    
    counter = 0
    while counter < len(chunk_to_send):
        stream_data = chunk_to_send[counter: min(counter + bufferSize,len(chunk_to_send))]
        counter += bufferSize
        TCP_Socket.send(stream_data.encode())
    
    TCP_Socket.send(end_msg.encode())



def recieve_chunk_over_TCP(TCP_Socket):
    start_chunk = TCP_Socket.recv(bufferSize).decode(errors='ignore') 
    if start_chunk == "":
        return (-2,"")
    
    
    chunk_index,chunk_len = [int(n) for n in start_chunk.split()]
    
    chunk_data = ""
    
    counter = 0
    while True:
        stream_data = TCP_Socket.recv(bufferSize + 256)
        if end_msg in stream_data.decode(errors='ignore'):
            chunk_data += stream_data.decode(errors='ignore').replace(end_msg,'')
            break
        chunk_data += stream_data.decode(errors='ignore')
        counter += bufferSize
    
    return (chunk_index,chunk_data)

# tcp_server_ports = generate_ports(n)
# udp_server_ports = generate_ports(n)

# tcp_client_ports = generate_ports(n)
# udp_client_ports = generate_ports(n)


