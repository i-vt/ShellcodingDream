"""Main encoder interface"""

import re
from encoders.xor import XOREncoder
from encoders.rot13 import ROT13Encoder
from encoders.base64 import Base64Encoder
from encoders.rc4 import RC4Encoder
from encoders.uuid import UUIDEncoder
from encoders.ip_address import IPAddressEncoder
from encoders.mac_address import MACAddressEncoder

class ShellcodeEncoder:
    """Unified interface for all encoders"""
    
    def __init__(self):
        self.encoders = {
            'xor': XOREncoder,
            'rot13': ROT13Encoder,
            'base64': Base64Encoder,
            'rc4': RC4Encoder,
            'uuid': UUIDEncoder,
            'ip': IPAddressEncoder,
            'mac': MACAddressEncoder,
        }
    
    def encode(self, technique, shellcode, key=None):
        """Encode shellcode with specified technique"""
        
        if technique not in self.encoders:
            raise ValueError(f"Unknown encoder: {technique}")
        
        # Parse shellcode
        if isinstance(shellcode, str):
            shellcode = self._parse_shellcode(shellcode)
        
        # Create encoder
        if technique in ['xor', 'rot13'] and key:
            encoder = self.encoders[technique](key=key)
        else:
            encoder = self.encoders[technique]()
        
        # Encode
        encoded = encoder.encode(shellcode)
        
        # Generate C code
        if isinstance(encoded, bytes):
            c_stub = encoder.generate_c_stub(encoded)
        else:
            c_stub = encoder.generate_c_stub(shellcode)
        
        return c_stub
    
    def _parse_shellcode(self, shellcode_str):
        """Parse shellcode from various formats"""
        
        shellcode_str = shellcode_str.strip()
        
        # Try \\x format
        if '\\x' in shellcode_str:
            matches = re.findall(r'\\x([0-9a-fA-F]{2})', shellcode_str)
            return bytes([int(m, 16) for m in matches])
        
        # Try space-separated
        if ' ' in shellcode_str:
            matches = re.findall(r'([0-9a-fA-F]{2})', shellcode_str)
            return bytes([int(m, 16) for m in matches])
        
        # Try continuous hex
        matches = re.findall(r'([0-9a-fA-F]{2})', shellcode_str)
        if matches:
            return bytes([int(m, 16) for m in matches])
        
        raise ValueError("Could not parse shellcode format")
