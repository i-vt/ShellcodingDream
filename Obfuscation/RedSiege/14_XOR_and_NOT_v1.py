# Obfuscation (Encryption) Code
def obfuscate_shellcode(shellcode, xor_key, increment):
    obfuscated = []
    for byte in shellcode:
        # XOR the byte with the key, then NOT it, and increment it
        obfuscated_byte = ~(byte ^ xor_key) + increment
        obfuscated.append(obfuscated_byte & 0xFF)  # Ensure it's within byte range (0-255)
    return bytes(obfuscated)

# Deobfuscation (Decryption) Code
def deobfuscate_shellcode(obfuscated_shellcode, xor_key, increment):
    deobfuscated = []
    for byte in obfuscated_shellcode:
        # Reverse the increment, NOT, and XOR process
        deobfuscated_byte = ~((byte - increment) & 0xFF) ^ xor_key
        deobfuscated.append(deobfuscated_byte & 0xFF)
    return bytes(deobfuscated)

# Example usage
if __name__ == "__main__":
    # Example shellcode
    shellcode = b"\x48\x31\xc0\x48\x89\xc2\x48\x89\xc6"  
    xor_key = 0x55  # Example XOR key
    increment = 1    # Example increment

    # Obfuscation (Encryption)
    obfuscated_shellcode = obfuscate_shellcode(shellcode, xor_key, increment)
    print("Obfuscated Shellcode:", obfuscated_shellcode)

    # Deobfuscation (Decryption)
    deobfuscated_shellcode = deobfuscate_shellcode(obfuscated_shellcode, xor_key, increment)
    print("Deobfuscated Shellcode:", deobfuscated_shellcode)

