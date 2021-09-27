import socket

for i in range(1025):
    try:
        print(f"{i}: {socket.getservbyport(i)}")
    except OSError:
        pass
