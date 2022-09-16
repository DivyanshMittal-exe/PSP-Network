n = 60

data_file = "A2_small_file.txt"
localIP     = "127.0.0.1"
# 
# bufferSize = chunkSize = 1024

chunkSize  = 1024
headerSize = 20
delimSize = 0
bufferSize = chunkSize + headerSize

data_for_chunk_count =  ""
# Here read as binary as non utf-8
with open(data_file, 'rb') as f:
    data_for_chunk_count = f.read()

chunk_count = len(data_for_chunk_count) //chunkSize

if  len(data_for_chunk_count)  % chunkSize != 0:
    chunk_count += 1

# print(chunk_count)
del data_for_chunk_count


end_message = "Done_quitting"
giving_chunk = "SendingChunk"
skip_mesaage = "Skip_Message"
req_chunk = "Req_Chunk"

exp_message = "Packet_Exp"


port   = 17000

server_tcp = port
port += 1

# server_tcp_ports = [i for i in range(port,port + n)]
# port += n

server_udp_ports = [i for i in range(port,port + n)]
port += n

tcp_client_ports = [i for i in range(port,port + n)]
port += n

udp_client_ports = [i for i in range(port,port + n)]
port += n




# chunk_addr_h = 10
# chunK_len_h = 10
# bufferSize = chunkSize + chunk_addr_h + chunK_len_h