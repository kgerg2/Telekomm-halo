import sys
import socket
import random
import struct
import time

server_addr = sys.argv[1]
server_port = int(sys.argv[2])

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect( (server_addr, server_port) )

ops = ['+', '-', '*', '/']

packer_with_length = struct.Struct('i i i c')
packer = struct.Struct('i i c')
#print(struct.calcsize('i i c'))
#vagy
#print(packer.size)

for nrnd in range(10):
	oper1 = random.randint(1,100)
	oper2 = random.randint(1,100)
	op = ops[nrnd % len(ops)]

	msg = packer_with_length.pack(struct.calcsize('i i c'), oper1, oper2, op.encode())
	print( "Üzenet: %d %c %d" % (oper1, op, oper2) )	
	sock.sendall( msg )

	msg = sock.recv(packer.size)
	parsed_msg = packer.unpack( msg )
	print( "Kapott eredmény: %d" % parsed_msg[0])
	time.sleep(2)
sock.close()


