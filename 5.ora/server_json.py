import sys
import socket
import struct
import select
import json

server_addr = sys.argv[1]
server_port = int(sys.argv[2])

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind( (server_addr, server_port) )

sock.listen(5)

ops = { '+': lambda x,y: x+y, 
    '-': lambda x,y: x-y,
    '*': lambda x,y: x*y,
    '/': lambda x,y: int(x/y)}
    
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
                parsed_msg = json.loads(msg.decode("utf-8"))
                print("A kliens üzenete: %d %c %d" % (parsed_msg['oper1'], parsed_msg['op'], parsed_msg['oper2']))
                result = {'result' : ops[parsed_msg['op']](parsed_msg['oper1'], parsed_msg['oper2'])}
                result = bytes(json.dumps(result), encoding = "utf-8")
                msg = packer_length.pack(len(result)) + result
                s.sendall(msg)
                print("Elküldött válasz:", result)
            
finally:
    sock.close()
