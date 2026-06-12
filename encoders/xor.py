"""XOR Encoding - Simple but effective"""

class XOREncoder:
    """Simple XOR encoding with configurable key"""
    
    def __init__(self, key=0xAA):
        self.key = key if isinstance(key, int) else int(key, 0)
    
    def encode(self, shellcode_bytes):
        """Encode shellcode with XOR"""
        return bytes([byte ^ self.key for byte in shellcode_bytes])
    
    def decode(self, encoded_bytes):
        """Decode XOR-encoded shellcode"""
        return bytes([byte ^ self.key for byte in encoded_bytes])
    
    def generate_c_stub(self, encoded_shellcode):
        """Generate C code snippet for XOR decoding"""
        hex_bytes = ', '.join([f'0x{b:02x}' for b in encoded_shellcode])
        
        c_code = f"""
// XOR Encoded Shellcode (Key: 0x{self.key:02x})
unsigned char shellcode[] = {{{hex_bytes}}};
unsigned int shellcode_len = sizeof(shellcode);

// XOR Decoder
void decode_shellcode() {{
    for (int i = 0; i < shellcode_len; i++) {{
        shellcode[i] ^= 0x{self.key:02x};
    }}
}}
"""
        return c_code
