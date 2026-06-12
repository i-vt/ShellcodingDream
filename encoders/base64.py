"""Base64 Encoding - Hide in plain sight"""

import base64

class Base64Encoder:
    """Base64 encoding for obfuscation"""
    
    def encode(self, shellcode_bytes):
        """Encode to base64"""
        return base64.b64encode(shellcode_bytes)
    
    def decode(self, encoded_data):
        """Decode from base64"""
        return base64.b64decode(encoded_data)
    
    def generate_c_stub(self, encoded_shellcode):
        """Generate C code for Base64 decoding"""
        base64_str = encoded_shellcode.decode('ascii') if isinstance(encoded_shellcode, bytes) else encoded_shellcode
        
        c_code = f'''
// Base64 Encoded Shellcode
const char* encoded_shellcode = 
    "{base64_str}";

// Note: Requires external Base64 decoder or custom implementation
unsigned char shellcode[2048];
int shellcode_len = 0;

void decode_shellcode() {{
    // Use custom Base64 decoder here
    // Or link against OpenSSL/crypto library
}}
'''
        return c_code
