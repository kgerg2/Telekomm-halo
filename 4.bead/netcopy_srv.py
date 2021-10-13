import hashlib
import sys
from socket import AF_INET, SOCK_STREAM, socket

BUFFER_SIZE = 1024

server_addr = (sys.argv[1], int(sys.argv[2]))
checksum_server_addr = (sys.argv[3], int(sys.argv[4]))
file_id = int(sys.argv[5])
file_path = sys.argv[6]

with socket(AF_INET, SOCK_STREAM) as server:
    server.bind(server_addr)
    server.listen(1)
    client, _ = server.accept()

    with open(file_path, "wb") as f:
        checksum = hashlib.md5()
        while data := client.recv(BUFFER_SIZE):
            f.write(data)
            checksum.update(data)

    client.close()

print(checksum.hexdigest())

with socket(AF_INET, SOCK_STREAM) as client:
    client.connect(checksum_server_addr)
    client.sendall(b"KI|%d" % file_id)
    reply = client.recv(BUFFER_SIZE)

checksum_length, checksum_rcv = reply.split(b"|")

print(checksum_rcv, checksum_length, checksum.hexdigest().encode())
if checksum_rcv and len(checksum_rcv) == int(checksum_length) and checksum_rcv == checksum.hexdigest().encode():
    print("CSUM OK")
else:
    print("CSUM CORRUPTED")
