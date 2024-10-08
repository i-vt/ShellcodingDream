import random
import struct

# RC4 key scheduling algorithm
def ksa(key):
    key_length = len(key)
    s = list(range(256))
    j = 0
    for i in range(256):
        j = (j + s[i] + key[i % key_length]) % 256
        s[i], s[j] = s[j], s[i]
    return s

# Pseudo-random generation algorithm (PRGA)
def prga(s):
    i = 0
    j = 0
    while True:
        i = (i + 1) % 256
        j = (j + s[i]) % 256
        s[i], s[j] = s[j], s[i]
        k = s[(s[i] + s[j]) % 256]
        yield k

# Encrypt/Decrypt using RC4
def rc4(key, data):
    s = ksa([ord(c) for c in key])
    keystream = prga(s)
    return bytes([c ^ next(keystream) for c in data])

# Example usage:
key = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz0123456789') for i in range(16))
data = b"Shellcode to be encrypted here"
encrypted_data = rc4(key, data)

print("Random Key:", key)
print("Encrypted Data:", encrypted_data.hex())

