"""
ShellcodingDream - Enhanced CLI Interface
Integrates all advanced evasion techniques
"""

import click
import sys
import os
from pathlib import Path
from tabulate import tabulate
from colorama import Fore, Back, Style, init

init(autoreset=True)

from app.encoder import ShellcodeEncoder
from app.compiler import ShellcodeCompiler
from app.validator import PayloadValidator
from evasion.injection import ProcessInjectionEngine
from evasion.packing import PackingEngine
from evasion.hooks import HookDetectionEngine, SyscallExtractor
from evasion.polymorphic import PolymorphicPayloadGenerator
from evasion.obfuscation import CodeObfuscator, ObfuscationLevel
from evasion.batch import BatchPayloadGenerator, BatchTester
from evasion.behavioral import BehavioralEvasion

BANNER = f"""
{Fore.CYAN}
╔═══════════════════════════════════════════════════════╗
║     ShellcodingDream - Advanced Edition               ║
║     Process Injection | Packing | Polymorphism       ║
║     Hook Detection | Code Obfuscation | Behavioral   ║
║     OSCP-Ready. Enterprise-Grade.                    ║
╚═══════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""

FEATURE_GROUPS = {
    'encoding': ['xor', 'rot13', 'base64', 'rc4', 'uuid', 'ip', 'mac'],
    'injection': ['dll', 'thread', 'hollow', 'apc'],
    'packing': ['upx', 'custom', 'hybrid'],
    'obfuscation': ['low', 'medium', 'high', 'maximum'],
    'evasion': ['low', 'medium', 'high'],
}


class ShellcodingCLI:
    """Enhanced CLI interface with all evasion techniques"""
    
    def __init__(self):
        self.encoder = ShellcodeEncoder()
        self.compiler = ShellcodeCompiler()
        self.validator = PayloadValidator()
        self.injection = ProcessInjectionEngine()
        self.packing = PackingEngine()
        self.hooks = HookDetectionEngine()
        self.syscalls = SyscallExtractor()
        self.polymorphic = PolymorphicPayloadGenerator()
        self.batch_gen = None
        self.behavioral = BehavioralEvasion()
    
    def show_features(self):
        """Show all available evasion features"""
        
        print(f"\n{Fore.GREEN}Advanced Evasion Features:{Style.RESET_ALL}\n")
        
        features = {
            'Process Injection': self.injection.get_supported_techniques(),
            'Packing Engines': self.packing.get_supported_packers(),
            'API Hooks Detection': self.hooks.hook_patterns,
            'Syscalls Available': dict(list(self.syscalls.windows_syscalls.items())[:5]),
            'Obfuscation Levels': self.show_obfuscation_levels(),
            'Behavioral Evasion': self.behavioral.get_evasion_techniques(),
        }
        
        for feature_name, details in features.items():
            print(f"{Fore.YELLOW}[{feature_name}]{Style.RESET_ALL}")
            if isinstance(details, dict):
                for k, v in details.items():
                    print(f"  • {k:20} - {v}")
            else:
                print(f"  {details}")
            print()
    
    @staticmethod
    def show_obfuscation_levels():
        """Show obfuscation levels"""
        return {
            'LOW': 'Dead code + control flow flattening',
            'MEDIUM': 'Variable renaming + constant splitting',
            'HIGH': 'Junk functions + string mangling',
            'MAXIMUM': 'State machine + anti-analysis',
        }


@click.group()
def cli():
    """ShellcodingDream - Advanced Evasion & Obfuscation"""
    print(BANNER)


# ════════════════════════════════════════════════════
# Original Commands (Preserved)
# ════════════════════════════════════════════════════

@cli.command()
def list():
    """List available encoders"""
    tool = ShellcodingCLI()
    tool.encoder.list_encoders()


@cli.command()
@click.option('--technique', required=True, type=click.Choice(['xor', 'rot13', 'base64', 'rc4', 'uuid', 'ip', 'mac']),
              help='Encoding technique')
@click.option('--input', required=True, type=click.Path(exists=True),
              help='Input shellcode file')
@click.option('--key', default=None,
              help='Encoding key')
@click.option('--output', default=None,
              help='Output file')
def encode(technique, input, key, output):
    """Encode shellcode"""
    tool = ShellcodingCLI()
    tool.encoder.quick_encode(technique, input, key=key, output=output)


# ════════════════════════════════════════════════════
# NEW: Process Injection Commands
# ════════════════════════════════════════════════════

@cli.group()
def inject():
    """Process injection techniques"""
    pass


@inject.command()
@click.option('--technique', type=click.Choice(['dll', 'thread', 'hollow', 'apc']),
              default='dll', help='Injection technique')
@click.option('--pid', type=int, required=True, help='Target process ID')
@click.option('--payload', required=True, type=click.Path(exists=True),
              help='DLL/shellcode file')
@click.option('--output', default=None, help='Output C file')
def create(technique, pid, payload, output):
    """Generate injection payload"""
    
    tool = ShellcodingCLI()
    
    print(f"{Fore.YELLOW}[*] Generating {technique} injection payload for PID {pid}...{Style.RESET_ALL}")
    
    c_code = tool.injection.generate_injection_payload(technique, pid, payload)
    
    if not output:
        output = f"injection_{technique}_{pid}.c"
    
    with open(output, 'w') as f:
        f.write(c_code)
    
    print(f"{Fore.GREEN}[+] Injection payload saved to: {output}{Style.RESET_ALL}")


# ════════════════════════════════════════════════════
# NEW: Packing Commands
# ════════════════════════════════════════════════════

@cli.group()
def pack():
    """Packing and compression"""
    pass


@pack.command()
@click.option('--technique', type=click.Choice(['upx', 'custom', 'hybrid']),
              default='upx', help='Packing technique')
@click.option('--input', required=True, type=click.Path(exists=True),
              help='Executable to pack')
@click.option('--output', default=None, help='Output packed file')
def binary(technique, input, output):
    """Pack executable"""
    
    tool = ShellcodingCLI()
    
    print(f"{Fore.YELLOW}[*] Packing with {technique}...{Style.RESET_ALL}")
    
    try:
        if technique == 'upx':
            result = tool.packing.pack_with_upx(input, output)
        elif technique == 'custom':
            # For custom, need shellcode input
            with open(input, 'rb') as f:
                shellcode = f.read()
            result = tool.packing.pack_with_custom_stub(shellcode, output)
        
        print(f"{Fore.GREEN}[+] Packed binary: {result}{Style.RESET_ALL}")
    
    except Exception as e:
        print(f"{Fore.RED}[!] Packing failed: {e}{Style.RESET_ALL}")
        sys.exit(1)


# ════════════════════════════════════════════════════
# NEW: Hook Detection Commands
# ════════════════════════════════════════════════════

@cli.group()
def detect():
    """Hook and API detection"""
    pass


@detect.command()
def hooks():
    """Generate hook detection code"""
    
    tool = ShellcodingCLI()
    
    c_code = tool.hooks.detect_iat_hooks()
    
    output = "hook_detector.c"
    with open(output, 'w') as f:
        f.write(c_code)
    
    print(f"{Fore.GREEN}[+] Hook detector saved to: {output}{Style.RESET_ALL}")


@detect.command()
@click.option('--syscall', default='NtCreateThreadEx',
              help='Syscall name')
@click.option('--arch', type=click.Choice(['x64', 'x86']),
              default='x64', help='Architecture')
@click.option('--output', default=None, help='Output file')
def syscall(syscall, arch, output):
    """Generate direct syscall code"""
    
    tool = ShellcodingCLI()
    
    c_code = tool.syscalls.generate_syscall_stub(syscall, arch)
    
    if not output:
        output = f"syscall_{syscall}_{arch}.c"
    
    with open(output, 'w') as f:
        f.write(c_code)
    
    print(f"{Fore.GREEN}[+] Syscall stub saved to: {output}{Style.RESET_ALL}")


# ════════════════════════════════════════════════════
# NEW: Polymorphic Commands
# ════════════════════════════════════════════════════

@cli.group()
def polymorphic():
    """Polymorphic payload generation"""
    pass


@polymorphic.command()
@click.option('--input', required=True, type=click.Path(exists=True),
              help='Shellcode hex file')
@click.option('--count', default=5, type=int,
              help='Number of variants')
@click.option('--output-dir', default='./polymorphic_variants',
              help='Output directory')
def batch(input, count, output_dir):
    """Generate polymorphic batch"""
    
    tool = ShellcodingCLI()
    
    print(f"{Fore.YELLOW}[*] Generating {count} polymorphic variants...{Style.RESET_ALL}")
    
    with open(input, 'r') as f:
        shellcode = f.read().strip()
    
    # Parse shellcode bytes
    import re
    hex_bytes = re.findall(r'\\x([0-9a-fA-F]{2})', shellcode)
    shellcode_bytes = bytes([int(h, 16) for h in hex_bytes])
    
    variants = tool.polymorphic.generate_polymorphic_batch(
        shellcode_bytes,
        count=count
    )
    
    os.makedirs(output_dir, exist_ok=True)
    
    for variant in variants:
        var_file = Path(output_dir) / f"{variant['id']}.c"
        with open(var_file, 'w') as f:
            f.write(variant['code'])
        print(f"[+] {variant['id']}")
    
    print(f"{Fore.GREEN}[+] Generated {count} variants in: {output_dir}{Style.RESET_ALL}")


# ════════════════════════════════════════════════════
# NEW: Obfuscation Commands
# ════════════════════════════════════════════════════

@cli.group()
def obfuscate():
    """Code obfuscation"""
    pass


@obfuscate.command()
@click.option('--input', required=True, type=click.Path(exists=True),
              help='C code file to obfuscate')
@click.option('--level', type=click.Choice(['low', 'medium', 'high', 'maximum']),
              default='medium', help='Obfuscation level')
@click.option('--output', default=None, help='Output file')
def code(input, level, output):
    """Obfuscate C code"""
    
    tool = ShellcodingCLI()
    
    level_map = {
        'low': ObfuscationLevel.LOW,
        'medium': ObfuscationLevel.MEDIUM,
        'high': ObfuscationLevel.HIGH,
        'maximum': ObfuscationLevel.MAXIMUM,
    }
    
    obfuscator = CodeObfuscator(level=level_map[level])
    
    with open(input, 'r') as f:
        c_code = f.read()
    
    print(f"{Fore.YELLOW}[*] Obfuscating with {level} level...{Style.RESET_ALL}")
    
    obfuscated = obfuscator.obfuscate_c_code(c_code)
    
    if not output:
        output = f"{Path(input).stem}_obfuscated_{level}.c"
    
    with open(output, 'w') as f:
        f.write(obfuscated)
    
    print(f"{Fore.GREEN}[+] Obfuscated code saved to: {output}{Style.RESET_ALL}")


# ════════════════════════════════════════════════════
# NEW: Batch Generation Commands
# ════════════════════════════════════════════════════

@cli.group()
def batch():
    """Batch payload generation"""
    pass


@batch.command()
@click.option('--input', required=True, type=click.Path(exists=True),
              help='Shellcode file')
@click.option('--techniques', multiple=True,
              default=['xor', 'rc4', 'base64'],
              help='Encoding techniques')
@click.option('--variants', default=3, type=int,
              help='Variants per technique')
@click.option('--output-dir', default='./batch_output',
              help='Output directory')
def generate(input, techniques, variants, output_dir):
    """Generate batch of payloads"""
    
    print(f"{Fore.YELLOW}[*] Generating batch payloads...{Style.RESET_ALL}")
    
    batch_gen = BatchPayloadGenerator(output_dir)
    
    with open(input, 'rb') as f:
        shellcode_bytes = f.read()
    
    manifest = batch_gen.generate_batch(shellcode_bytes, techniques, variants)
    
    print(f"{Fore.GREEN}[+] Batch generation complete{Style.RESET_ALL}")


# ════════════════════════════════════════════════════
# NEW: Behavioral Evasion Commands
# ════════════════════════════════════════════════════

@cli.group()
def evasion():
    """Behavioral evasion techniques"""
    pass


@evasion.command()
@click.option('--level', type=click.Choice(['low', 'medium', 'high']),
              default='high', help='Evasion level')
@click.option('--output', default=None, help='Output C file')
def behavioral(level, output):
    """Generate behavioral evasion code"""
    
    tool = ShellcodingCLI()
    
    print(f"{Fore.YELLOW}[*] Generating {level} behavioral evasion code...{Style.RESET_ALL}")
    
    stub = tool.behavioral.generate_full_evasion_stub(level)
    
    if not output:
        output = f"evasion_stub_{level}.c"
    
    with open(output, 'w') as f:
        f.write(stub)
    
    print(f"{Fore.GREEN}[+] Evasion stub saved to: {output}{Style.RESET_ALL}")


# ════════════════════════════════════════════════════
# NEW: Feature Overview
# ════════════════════════════════════════════════════

@cli.command()
def features():
    """Show all available features"""
    
    tool = ShellcodingCLI()
    tool.show_features()


@cli.command()
def guide():
    """Show comprehensive usage guide"""
    
    guide_text = f"""
{Fore.CYAN}╔═════════════════════════════════════════════════════╗
║   ShellcodingDream Advanced Features Guide            ║
╚═════════════════════════════════════════════════════════╝{Style.RESET_ALL}

{Fore.GREEN}1. PROCESS INJECTION{Style.RESET_ALL}
   Generate code for multiple injection techniques:
   
   shellcoding inject create --technique dll --pid 1234 --payload payload.dll
   shellcoding inject create --technique hollow --pid 1234 --payload calc.exe

   Supported: dll, thread hijacking, process hollowing, APC

{Fore.GREEN}2. PACKING{Style.RESET_ALL}
   Pack executables for evasion:
   
   shellcoding pack binary --technique upx --input payload.exe
   shellcoding pack binary --technique custom --input payload.exe

{Fore.GREEN}3. HOOK DETECTION{Style.RESET_ALL}
   Generate hook detection and API bypass code:
   
   shellcoding detect hooks           # Generate hook detector
   shellcoding detect syscall --syscall NtCreateThreadEx

{Fore.GREEN}4. POLYMORPHIC PAYLOADS{Style.RESET_ALL}
   Generate unique variants automatically:
   
   shellcoding polymorphic batch --input payload.hex --count 10

{Fore.GREEN}5. CODE OBFUSCATION{Style.RESET_ALL}
   Apply advanced obfuscation:
   
   shellcoding obfuscate code --input shellcode.c --level maximum

{Fore.GREEN}6. BATCH GENERATION{Style.RESET_ALL}
   Create payload batches efficiently:
   
   shellcoding batch generate --input payload.hex --techniques xor rc4 base64

{Fore.GREEN}7. BEHAVIORAL EVASION{Style.RESET_ALL}
   Add anti-debug, anti-VM, anti-sandbox:
   
   shellcoding evasion behavioral --level high

{Fore.YELLOW}OSCP Quick Reference:{Style.RESET_ALL}

# Standard pipeline (unchanged)
shellcoding pipeline --technique xor --input payload.hex --platform linux

# Advanced pipeline with evasion
shellcoding encode --technique xor --input payload.hex
shellcoding obfuscate code --input encoded.c --level high
shellcoding polymorphic batch --input payload.hex --count 5

"""
    
    print(guide_text)


def main():
    """Entry point"""
    try:
        cli()
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        sys.exit(1)


if __name__ == '__main__':
    main()
