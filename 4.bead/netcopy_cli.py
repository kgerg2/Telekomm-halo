import hashlib
import sys
from socket import AF_INET, SOCK_STREAM, socket

BUFFER_SIZE = 1024

server_addr = (sys.argv[1], int(sys.argv[2]))
checksum_server_addr = (sys.argv[3], int(sys.argv[4]))
file_id = int(sys.argv[5])
file_path = sys.argv[6]

with socket(AF_INET, SOCK_STREAM) as client:
    client.connect(server_addr)

    with open(file_path, "rb") as f:
        checksum = hashlib.md5()
        while data := f.read(BUFFER_SIZE):
            client.sendall(data)
            checksum.update(data)

checksum_bytes = checksum.hexdigest().encode()
msg = b"BE|%d|%d|%d|%b" % (file_id, 60, len(checksum_bytes), checksum_bytes)
print(msg)

with socket(AF_INET, SOCK_STREAM) as client:
    client.connect(checksum_server_addr)
    client.sendall(msg)
    reply = client.recv(BUFFER_SIZE)

    if reply != b"OK":
        print(f"Valami hiba történt. (kapott válasz: {reply})")
