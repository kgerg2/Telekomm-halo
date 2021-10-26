import socket
import struct

address = ('localhost', 10000)
map_bank_server_address = ('localhost', 10001)

packer = struct.Struct("i i i i 6s")


with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
    server.bind(address)

    while True:
        try:
            data, claddr = server.recvfrom(packer.size)

            print(f"Üzenet {claddr}-től: {packer.unpack(data)}")

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.connect(map_bank_server_address)
                client.sendall(data)
                reply = client.recv(struct.calcsize("i i"))

            print("Válasz:", struct.unpack("i i", reply))

            server.sendto(reply, claddr)

        except KeyboardInterrupt:
            break
