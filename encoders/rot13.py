"""ROT13 Caesar Cipher Encoding"""

class ROT13Encoder:
    """Caesar cipher with configurable rotation"""
    
    def __init__(self, rotation=13):
        self.rotation = rotation % 256
    
    def encode(self, shellcode_bytes):
        """Encode with Caesar cipher"""
        return bytes([((byte + self.rotation) % 256) for byte in shellcode_bytes])
    
    def decode(self, encoded_bytes):
        """Decode Caesar cipher"""
        return bytes([((byte - self.rotation) % 256) for byte in encoded_bytes])
    
    def generate_c_stub(self, encoded_shellcode):
        """Generate C code for ROT13 decoding"""
        hex_bytes = ', '.join([f'0x{b:02x}' for b in encoded_shellcode])
        
        c_code = f"""
// ROT13 Encoded Shellcode (Rotation: {self.rotation})
unsigned char shellcode[] = {{{hex_bytes}}};
unsigned int shellcode_len = sizeof(shellcode);

// ROT13 Decoder
void decode_shellcode() {{
    for (int i = 0; i < shellcode_len; i++) {{
        shellcode[i] = (shellcode[i] - {self.rotation}) % 256;
    }}
}}
"""
        return c_code
