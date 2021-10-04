import socket
from struct import calcsize, pack, unpack

TCP_IP = 'localhost'
TCP_PORT = 10000
BUFFER_SIZE = 1024
format = "i i 1s"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((TCP_IP, TCP_PORT))

def calculate(x, y, op):
    op = op.decode()
    if isinstance(x, int) and isinstance(y, int) and op in "+-*/":
        return int(eval(f"{x} {op} {y}"))
    
    raise ValueError

while True:
    try:
        data, client = sock.recvfrom(calcsize(format))
        print('Valaki csatlakozott:', client)    
        print("Üzenet:", data)

        result = calculate(*unpack(format, data))

        print(f"{result=}")

        sock.sendto(pack("i", result), client)
    except KeyboardInterrupt:
        break

sock.close()
