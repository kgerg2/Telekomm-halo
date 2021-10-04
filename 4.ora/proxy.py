import select
import socket
import struct
from struct import calcsize, pack, unpack

TCP_IP = 'localhost'
TCP_PORT = 10001
format = "i i 1s"
packer = struct.Struct(format)
server = ('localhost', 10000)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((TCP_IP, TCP_PORT))

sock.listen(5)

inputs = [sock]
proxy_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


while True:
    try:
        readables, _, _ = select.select(inputs, [], [])

        for s in readables:
            if s is sock:
                connection, client_info = sock.accept()
                print(f"Csatlakozott {client_info}")
                inputs.append(connection)
            else:
                msg = s.recv(packer.size)

                if not msg:
                    s.close()
                    print("Valaki kilépett")
                    inputs.remove(s)
                    continue

                x, y, op = packer.unpack(msg)
                print(f"{x=}, {y=}, {op=}")
                proxy_sock.connect(server)
                proxy_sock.send(packer.pack(2*x, y+1, op))
                reply = proxy_sock.recv(calcsize("i"))
                proxy_sock.close()
                print(reply, len(reply))
                print(f"Elküldött válasz: {unpack('i', reply)}")
                s.sendall(reply)
                
    except Exception as e:
        for s in inputs:
            s.close()
        print("Server closing")
        raise e
        break
