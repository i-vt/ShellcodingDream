import random
import argparse
# pip3 install pycryptodome
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os

# Sample shellcode for testing
shellcode = bytearray([0xfc, 0x48, 0x83, 0xe4, 0xf0, 0xe8, 0xc0, 0x00, 0x00, 0x00])

# XOR Encryption with Single Byte Key
def xor_single_byte(shellcode, key):
    print(f"Original Shellcode: {shellcode}")
    encrypted_shellcode = bytearray([b ^ key for b in shellcode])
    print(f"Encrypted Shellcode with XOR key {key}: {encrypted_shellcode}")
    return encrypted_shellcode

# XOR Encryption with Multi-Byte Key
def xor_multi_byte(shellcode, key):
    print(f"Original Shellcode: {shellcode}")
    key_len = len(key)
    encrypted_shellcode = bytearray([shellcode[i] ^ key[i % key_len] for i in range(len(shellcode))])
    print(f"Encrypted Shellcode with Multi-byte XOR key: {encrypted_shellcode}")
    return encrypted_shellcode

# AES Encryption
def aes_encrypt(shellcode, key):
    print(f"Original Shellcode: {shellcode}")
    iv = os.urandom(16)  # Initialization Vector
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_shellcode = iv + cipher.encrypt(pad(shellcode, AES.block_size))
    print(f"Encrypted Shellcode with AES: {encrypted_shellcode}")
    return encrypted_shellcode

# AES Decryption
def aes_decrypt(encrypted_shellcode, key):
    iv = encrypted_shellcode[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_shellcode = unpad(cipher.decrypt(encrypted_shellcode[16:]), AES.block_size)
    print(f"Decrypted Shellcode: {decrypted_shellcode}")
    return decrypted_shellcode

def main():
    parser = argparse.ArgumentParser(description="Shellcode encryption techniques demo")
    parser.add_argument('-m', '--method', type=str, required=True, help="Choose the encryption method: xor_single, xor_multi, aes")
    parser.add_argument('-k', '--key', type=str, help="Encryption key for XOR multi-byte or AES", required=False)
    parser.add_argument('-s', '--shellcode', type=str, help="Path to shellcode file (default uses embedded shellcode)", required=False)
    
    args = parser.parse_args()

    # Load shellcode if provided, otherwise use the default
    if args.shellcode:
        with open(args.shellcode, 'rb') as f:
            shellcode = bytearray(f.read())
    
    if args.method == "xor_single":
        key = random.randint(1, 255)  # Generate random single-byte XOR key
        print(f"Using XOR Single Byte Key: {key}")
        encrypted = xor_single_byte(shellcode, key)
        print(f"XOR Encrypted Shellcode: {encrypted}")
    
    elif args.method == "xor_multi":
        if not args.key:
            print("Please provide a multi-byte key using the -k option")
            return
        multi_byte_key = args.key.encode('utf-8')
        print(f"Using XOR Multi-Byte Key: {multi_byte_key}")
        encrypted = xor_multi_byte(shellcode, multi_byte_key)
        print(f"XOR Multi-Byte Encrypted Shellcode: {encrypted}")

    elif args.method == "aes":
        if not args.key or len(args.key) != 16:
            print("Please provide a 16-byte AES key using the -k option")
            return
        aes_key = args.key.encode('utf-8')
        encrypted = aes_encrypt(shellcode, aes_key)
        print(f"AES Encrypted Shellcode: {encrypted}")
        # Decrypt to verify
        decrypted = aes_decrypt(encrypted, aes_key)
        print(f"AES Decrypted Shellcode: {decrypted}")
    
    else:
        print("Invalid method. Choose 'xor_single', 'xor_multi', or 'aes'.")

if __name__ == "__main__":
    main()

