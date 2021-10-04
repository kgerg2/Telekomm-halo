import hashlib

m = hashlib.md5("Nobody expects".encode())
m.update(b" the spanish inquisition")
print("Digest: {}".format(m.digest()))
print("Digest in hex: 0x{}".format(m.hexdigest()))
print("Digest size: {}".format(m.digest_size))

another = hashlib.md5(b"Nobody expects the spanish inquisition")
print("\nAnother Digest : {}".format(another.digest()))

yetAnother = hashlib.md5(b"Kecske")
print("\nyetAnother Digest size: {}".format(yetAnother.digest_size))

# 16 bájt hosszú eredmény
