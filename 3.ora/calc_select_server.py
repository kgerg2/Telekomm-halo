import socket
import select
import struct

TCP_IP = 'localhost'
TCP_PORT = 10000
BUFFER_SIZE = 1024
format = "i i 1s"
packer = struct.Struct(format)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((TCP_IP, TCP_PORT))

sock.listen(5)

inputs = [sock]

def calculate(x, y, op):
    op = op.decode()
    if isinstance(x, int) and isinstance(y, int) and op in "+-*/":
        return int(eval(f"{x} {op} {y}"))
    
    raise ValueError

while True:
    try:
        readables, _, _ = select.select(inputs, [], [])

        for s in readables:
            if s in sock:
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

                parsed = packer.unpack(msg)
                print(f"{parsed=}")

    except Exception as e:
        print(e)


    conn, addr = sock.accept()
    print('Valaki csatlakozott:', addr)

    data = conn.recv(calcsize(format))
    
    if not data:
        break
    print("Üzenet:", data)
    result = calculate(*unpack(format, data))
    print(f"{result=}")
    conn.send(pack("i", result))

conn.close()
sock.close()
