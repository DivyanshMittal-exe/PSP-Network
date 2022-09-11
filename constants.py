import socket

n = 5

data_file = "Small.txt"
localIP     = "127.0.0.1"
chunkSize  = 1024
header = 20
bufferSize = chunkSize + header

data =  ""
# Here read as binary as non utf-8
with open(data_file, 'r', encoding='utf-8') as f:
    data = f.read()

chunk_count = len(data) //1024

if  len(data)  % 1024 != 0:
    chunk_count += 1

# print(chunk_count)
del data

# print(chunk_count)
end_msg = "Done_quitting"
end_msg = end_msg.ljust(bufferSize)


hab = "I have"
nthab = "I not have"

skip_chunk = "Skip Chunk !=!"
skip_chunk = skip_chunk.ljust(bufferSize)

ign_message = "I dont have it"
ign_message = ign_message.ljust(bufferSize)

port   = 31580

server_tcp = port
port += 1


server_udp = port
port += 1

tcp_client_ports = [i for i in range(port,port + n)]
port += n

udp_client_ports = [i for i in range(port,port + n)]
port += n


def getTCPmessage(TCPSocket):
    
    # print("Here")
    
    packet = ""
    len_left = bufferSize - len(packet)
    
    while len_left != 0:
        message = TCPSocket.recv(len_left).decode()
        packet += message
        len_left = bufferSize - len(packet)
        
    # print("Left here")
    # assert len(packet) == bufferSize
    print(packet[:10])
    return packet


def send_chunk_over_TCP(sender_tcp,reciever_tcp,chunk_to_send):
    
    TCP_Socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    TCP_Socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    TCP_Socket.bind((localIP, sender_tcp)) 
    
    TCP_Socket.connect((localIP,reciever_tcp))

    TCP_Socket.send(chunk_to_send.encode())

    TCP_Socket.shutdown(socket.SHUT_RDWR)
    TCP_Socket.close()
    
def recieve_chunk_over_TCP(reciever_socket,time_out = 10):
    
    TCP_Socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    TCP_Socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    TCP_Socket.bind((localIP, reciever_socket))    
    
    TCP_Socket.listen(n)
    
    if time_out != None:
        TCP_Socket.settimeout(time_out)
    try:
        connectionSocket, addr = TCP_Socket.accept()
        TCP_Socket.setblocking(1) 
        start_chunk = getTCPmessage(connectionSocket)
    except:
        start_chunk = -1
    
  
    # print(chunk_data[0:100])
    TCP_Socket.shutdown(socket.SHUT_RDWR)
    TCP_Socket.close()
    return start_chunk