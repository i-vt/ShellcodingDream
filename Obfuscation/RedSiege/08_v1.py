import uuid

# Function to read shellcode and convert it into a list of UUIDs
def shellcode_to_uuids(shellcode):
    uuids = []
    # Read the shellcode in 16-byte chunks
    for i in range(0, len(shellcode), 16):
        chunk = shellcode[i:i + 16]
        # Pad with NOPs (0x90) if the chunk is less than 16 bytes
        if len(chunk) < 16:
            chunk += b'\x90' * (16 - len(chunk))
        # Convert the chunk to a UUID
        uuid_val = uuid.UUID(bytes_le=chunk)  # Use little-endian byte order
        uuids.append(str(uuid_val))
    return uuids

# Sample shellcode (this would be your actual shellcode)
shellcode = b"\xfc\x48\x83\xe4\xf0\xe8\x00\x00\x00\x00\x41\x51\x41\x50"

# Convert shellcode to UUIDs
uuids = shellcode_to_uuids(shellcode)

# Print the UUIDs
for u in uuids:
    print(u)

