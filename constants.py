import socket
import random

port_number = 4000

def check_port(port):
    with socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) as s:
        return s.connect_ex((localIP, port)) == 0

def generate_ports(size):
    global port_number
    ports = []
    while len(ports) < size:
        if check_port(port_number):
           ports.append(port_number)
        port_number += 1
    return ports

n = 5
data_file = "A2_small_file.txt"
localIP     = "127.0.0.1"
port   = 20020 
bufferSize  = 1024

recv_extra = 256

end_msg = "Done_quitting"

tcp_server_ports = [i for i in range(port,port + n)]
port += n

udp_server_ports = [i for i in range(port,port + n)]
port += n

tcp_client_ports = [i for i in range(port,port + n)]
port += n

udp_client_ports = [i for i in range(port,port + n)]
port += n


# tcp_server_ports = generate_ports(n)
# udp_server_ports = generate_ports(n)

# tcp_client_ports = generate_ports(n)
# udp_client_ports = generate_ports(n)

server_tcp = 20102
server_udp = 20079
