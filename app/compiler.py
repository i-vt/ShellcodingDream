"""C code compilation interface"""

import subprocess
import os
import tempfile
from pathlib import Path

class ShellcodeCompiler:
    """Compile C code to binaries"""
    
    def __init__(self):
        self.gcc_flags_linux = ['-fno-stack-protector', '-z execstack', '-O0']
        self.gcc_flags_windows = ['-static']
    
    def compile(self, c_code, technique, arch='x64', platform='linux', output=None):
        """Compile C code to binary"""
        
        # Create temporary C file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.c', delete=False) as f:
            f.write(c_code)
            c_file = f.name
        
        try:
            # Determine output filename
            if not output:
                output = f"payload_{technique}_{arch}"
            
            # Build compiler command
            if platform == 'windows':
                cc = 'x86_64-w64-mingw32-gcc'
                if arch == 'x86':
                    cc = 'i686-w64-mingw32-gcc'
            else:
                cc = 'gcc'
            
            flags = self.gcc_flags_linux if platform == 'linux' else self.gcc_flags_windows
            
            cmd = [cc] + flags + ['-o', output, c_file]
            
            # Compile
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode != 0:
                raise RuntimeError(f"Compilation failed:\n{result.stderr}")
            
            return output
            
        finally:
            # Cleanup temp file
            os.unlink(c_file)
