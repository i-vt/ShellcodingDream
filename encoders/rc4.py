"""RC4 Stream Cipher Encoding"""

class RC4Encoder:
    """RC4 cipher implementation"""
    
    def __init__(self, key=b'ShellcodingDream'):
        self.key = key if isinstance(key, bytes) else key.encode()
    
    def ksa(self, key):
        """Key Scheduling Algorithm"""
        S = list(range(256))
        j = 0
        
        for i in range(256):
            j = (j + S[i] + key[i % len(key)]) % 256
            S[i], S[j] = S[j], S[i]
        
        return S
    
    def prga(self, S, length):
        """Pseudo-Random Generation Algorithm"""
        i = j = 0
        K = []
        
        for _ in range(length):
            i = (i + 1) % 256
            j = (j + S[i]) % 256
            S[i], S[j] = S[j], S[i]
            K.append(S[(S[i] + S[j]) % 256])
        
        return bytes(K)
    
    def encode(self, shellcode_bytes):
        """RC4 encode"""
        S = self.ksa(self.key)
        keystream = self.prga(S, len(shellcode_bytes))
        return bytes([a ^ b for a, b in zip(shellcode_bytes, keystream)])
    
    def decode(self, encoded_bytes):
        """RC4 decode (same as encode)"""
        return self.encode(encoded_bytes)
    
    def generate_c_stub(self, encoded_shellcode):
        """Generate C code for RC4 decoding"""
        hex_bytes = ', '.join([f'0x{b:02x}' for b in encoded_shellcode])
        key_hex = ', '.join([f'0x{b:02x}' for b in self.key])
        
        c_code = f"""
// RC4 Encoded Shellcode
unsigned char shellcode[] = {{{hex_bytes}}};
unsigned char rc4_key[] = {{{key_hex}}};
int shellcode_len = sizeof(shellcode);

// RC4 Key Scheduling
void rc4_ksa(unsigned char *S, unsigned char *key, int keylen) {{
    for (int i = 0; i < 256; i++)
        S[i] = i;
    
    int j = 0;
    for (int i = 0; i < 256; i++) {{
        j = (j + S[i] + key[i % keylen]) % 256;
        unsigned char tmp = S[i];
        S[i] = S[j];
        S[j] = tmp;
    }}
}}

// RC4 PRGA
unsigned char rc4_byte(unsigned char *S, int *i, int *j) {{
    *i = (*i + 1) % 256;
    *j = (*j + S[*i]) % 256;
    unsigned char tmp = S[*i];
    S[*i] = S[*j];
    S[*j] = tmp;
    return S[(S[*i] + S[*j]) % 256];
}}

// RC4 Decoder
void decode_shellcode() {{
    unsigned char S[256];
    rc4_ksa(S, rc4_key, sizeof(rc4_key));
    
    int i = 0, j = 0;
    for (int k = 0; k < shellcode_len; k++)
        shellcode[k] ^= rc4_byte(S, &i, &j);
}}
"""
        return c_code
