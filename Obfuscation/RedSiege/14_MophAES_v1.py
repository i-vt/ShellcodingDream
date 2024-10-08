from Crypto.Cipher import AES
import os

# AES key and IV generation
def generate_key_iv():
    key = os.urandom(32)  # AES-256 key size
    iv = os.urandom(16)   # AES block size (128-bit)
    return key, iv

# Polymorphic encryption
def polymorphic_encrypt(shellcode, key, iv):
    # Create AES cipher
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    # Padding to match AES block size
    padding_length = AES.block_size - len(shellcode) % AES.block_size
    padded_shellcode = shellcode + bytes([padding_length]) * padding_length
    
    # Encrypt shellcode
    encrypted_shellcode = cipher.encrypt(padded_shellcode)
    
    # Modify constants to add polymorphism (this is a simple example)
    constant_modifier = os.urandom(1)[0]
    encrypted_shellcode = bytes([b ^ constant_modifier for b in encrypted_shellcode])
    
    return encrypted_shellcode, constant_modifier

# Polymorphic decryption
def polymorphic_decrypt(encrypted_shellcode, key, iv, constant_modifier):
    # Reverse the polymorphic constant modification
    encrypted_shellcode = bytes([b ^ constant_modifier for b in encrypted_shellcode])
    
    # Create AES cipher
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    # Decrypt shellcode
    decrypted_shellcode = cipher.decrypt(encrypted_shellcode)
    
    # Remove padding
    padding_length = decrypted_shellcode[-1]
    decrypted_shellcode = decrypted_shellcode[:-padding_length]
    
    return decrypted_shellcode

# Example usage
if __name__ == "__main__":
    # Example shellcode
    shellcode = b"\x48\x31\xc0\x48\x89\xc2\x48\x89\xc6"
    
    # Generate AES key and IV
    key, iv = generate_key_iv()
    
    # Encrypt shellcode
    encrypted_shellcode, constant_modifier = polymorphic_encrypt(shellcode, key, iv)
    print(f"Encrypted Shellcode: {encrypted_shellcode}")
    
    # Decrypt shellcode
    decrypted_shellcode = polymorphic_decrypt(encrypted_shellcode, key, iv, constant_modifier)
    print(f"Decrypted Shellcode: {decrypted_shellcode}")

