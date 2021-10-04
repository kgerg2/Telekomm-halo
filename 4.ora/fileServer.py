from socket import socket, AF_INET, SOCK_STREAM
import sys

server_addr = (sys.argv[1], int(sys.argv[2]))

with socket(AF_INET, SOCK_STREAM) as server:
    server.bind(server_addr)
    server.listen(1)

    client, client_addr = server.accept()

    with open(sys.argv[3], "wb") as f:
        while data := client.recv(128):
            f.write(data)
            
    client.close()

print("Sikerült!")
