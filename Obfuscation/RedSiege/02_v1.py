# Caesar cipher (ROT13) for shellcode obfuscation
def caesar_cipher_encrypt(shellcode):
    encrypted_shellcode = []
    for byte in shellcode:
        # Apply ROT13 (shift by 13)
        encrypted_byte = (byte + 13) % 256  # Ensure byte stays within 0-255
        encrypted_shellcode.append(encrypted_byte)
    return encrypted_shellcode

def caesar_cipher_decrypt(encrypted_shellcode):
    decrypted_shellcode = []
    for byte in encrypted_shellcode:
        # Reverse ROT13 (subtract 13)
        decrypted_byte = (byte - 13) % 256  # Ensure byte stays within 0-255
        decrypted_shellcode.append(decrypted_byte)
    return decrypted_shellcode

# Example shellcode (hex values)
original_shellcode = [0xFC, 0x48, 0x83, 0xE4, 0xF0]  # Example shellcode

print("Original shellcode: ")
print(' '.join([f'{byte:02X}' for byte in original_shellcode]))

# Encrypt the shellcode using ROT13
encrypted_shellcode = caesar_cipher_encrypt(original_shellcode)
print("\nEncrypted shellcode (ROT13): ")
print(' '.join([f'{byte:02X}' for byte in encrypted_shellcode]))

# Decrypt the shellcode back to original
decrypted_shellcode = caesar_cipher_decrypt(encrypted_shellcode)
print("\nDecrypted shellcode (back to original): ")
print(' '.join([f'{byte:02X}' for byte in decrypted_shellcode]))

# Check if the decryption worked correctly
assert original_shellcode == decrypted_shellcode, "Decryption failed!"

