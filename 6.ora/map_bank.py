import random
import select
import socket
import struct

address = ('localhost', 10001)

packer = struct.Struct("i i i i 6s")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(address)

sock.listen(1)

times = {(0, 0): 75}

inputs = [sock]

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

                coord1, coord2, hour, min, neptun = packer.unpack(msg)

                arrival = hour * 60 + min + times.get((coord1, coord2), random.randint(1, 120))

                reply = struct.pack("i i", arrival // 60, arrival % 60)

                s.sendall(reply)

                print(f"Elküldött válasz: {struct.unpack('i i', reply)}")

    except Exception as e:
        for s in inputs:
            s.close()
        print("Server closing")
        raise e
        break
