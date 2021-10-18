import sys
import socket
import struct
import select

server_addr = sys.argv[1]
server_port = int(sys.argv[2])

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind( (server_addr, server_port) )

sock.listen(5)

ops = { '+': lambda x,y: x+y, 
    '-': lambda x,y: x-y,
    '*': lambda x,y: x*y,
    '/': lambda x,y: int(x/y)}

packer = struct.Struct('i i c')
packer_length = struct.Struct('i')

inputs = [ sock ]

try:
    while True:
        readables, _, _ = select.select( inputs, [], [] )
        
        for s in readables:
            if s is sock:
                connection, client_info = sock.accept()
                print("Csatlakozott valaki: %s:%d" % client_info )
                inputs.append(connection)
            else:
                msg = s.recv(packer_length.size)
                if not msg:
                    s.close()
                    print("A kliens lezárta a kapcsolatot")
                    inputs.remove(s)
                    continue
                length = packer_length.unpack(msg)[0]
                msg = s.recv(length)
                parsed_msg = packer.unpack(msg)
                print("A kliens üzenete: %d %c %d" % (parsed_msg[0], parsed_msg[2].decode(), parsed_msg[1]))
                result = ops[parsed_msg[2].decode()](parsed_msg[0], parsed_msg[1])
                msg = packer.pack(result, 0, b'R')
                s.sendall(msg)
                print("Elküldött válasz: %d" % result)
            
finally:
    sock.close()
