import socket
from struct import calcsize, pack, unpack

TCP_IP = 'localhost'
TCP_PORT = 10000
BUFFER_SIZE = 1024
format = "i i 1s"

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((TCP_IP, TCP_PORT))

def calculate(x, y, op):
    op = op.decode()
    if isinstance(x, int) and isinstance(y, int) and op in "+-*/":
        return int(eval(f"{x} {op} {y}"))
    
    raise ValueError

while True:
    sock.listen(1)

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
