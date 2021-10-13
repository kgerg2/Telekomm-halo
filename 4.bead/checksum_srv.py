import select
import socket
import sys
import time
from bisect import insort
from itertools import dropwhile, takewhile

BUFFER_SIZE = 1024
server_addr = (sys.argv[1], int(sys.argv[2]))

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(server_addr)

sock.listen(1)

exp_times = []
checksums = {}  # file_id: (expiry time, checksum length, checksum)

inputs = [sock]

while True:
    try:
        readables, _, _ = select.select(inputs, [], [])

        for s in readables:
            if s is sock:
                connection, client_info = sock.accept()
                inputs.append(connection)
            else:
                msg = s.recv(BUFFER_SIZE)

                if not msg:
                    s.close()
                    inputs.remove(s)
                    continue

                intent, file_id, *param = msg.split(b"|")
                file_id = int(file_id)

                if intent == b"BE":
                    ttl, checksum_len, checksum = param
                    exp_time = time.time() + int(ttl)

                    if file_id in checksums:
                        exp_times.remove((checksums[file_id][0], file_id))

                    insort(exp_times, (exp_time, file_id))
                    checksums[file_id] = (exp_time, checksum_len, checksum)

                    if int(checksum_len) != len(checksum):
                        print(f"Unexpected checksum: '{checksum}' with length {checksum_len}")

                    reply = b"OK"
                elif intent == b"KI":
                    if file_id in checksums:
                        reply = b"|".join(checksums.pop(file_id)[1:])
                    else:
                        reply = b"0|"
                else:
                    print(f"Unexpected intent: '{intent}' (message: '{msg}')")

                s.sendall(reply)

                for _, file_id in takewhile(lambda x: x[0] < time.time(), exp_times):
                    checksums.pop(file_id)

                exp_times = list(dropwhile(lambda x: x[0] < time.time(), exp_times))
    except Exception as e:
        for s in inputs:
            s.close()
        break
