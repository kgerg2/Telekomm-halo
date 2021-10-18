import sys
import socket
import random
import struct
import time
import json

server_addr = sys.argv[1]
server_port = int(sys.argv[2])

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect( (server_addr, server_port) )

ops = ['+', '-', '*', '/']

packer_length = struct.Struct('i')
#print(struct.calcsize('i i c'))
#vagy
#print(packer.size)

for nrnd in range(10):
    oper1 = random.randint(1,100)
    oper2 = random.randint(1,100)
    op = ops[nrnd % len(ops)]
    
    data = {'oper1' : oper1, 'oper2' : oper2, 'op' : op}
    msg_json = json.dumps(data)
    msg = packer_length.pack(len(msg_json)) + bytes(msg_json, encoding = 'utf-8')
    print( "Üzenet: %d %c %d" % (oper1, op, oper2) )    
    sock.sendall( msg )

    msg = sock.recv(packer_length.size)
    length = packer_length.unpack(msg)[0]
    msg = sock.recv(length)
    parsed_msg = json.loads(msg.decode("utf-8"))
    print( "Kapott eredmény:", parsed_msg)
    time.sleep(2)
sock.close()


