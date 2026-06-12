#!/usr/bin/env python3
"""
ShellcodingDream - Dockerized Shellcode Obfuscation Tool
OSCP-Ready. One command. All encoders.
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

BANNER = f"""
{Fore.CYAN}
╔═══════════════════════════════════════════════════════╗
║     ShellcodingDream - Dockerized Edition            ║
║     One Tool. All Encoders. OSCP-Ready.              ║
╚═══════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""

ENCODERS = {
    'xor': 'Simple XOR cipher - fastest, works 70% of the time',
    'rot13': 'Caesar cipher ROT13 - simple substitution',
    'base64': 'Base64 encoding - hides in plain sight',
    'rc4': 'RC4 stream cipher - stronger encryption',
    'uuid': 'Encode as UUIDs - evades pattern matching',
    'ip': 'Encode as IP addresses - looks like network config',
    'mac': 'Encode as MAC addresses - looks innocent',
}

PAYLOADS = {
    'linux_reverse_tcp': 'Linux x64 reverse shell',
    'linux_bind_tcp': 'Linux x64 bind shell',
    'windows_reverse_tcp': 'Windows x64 reverse shell',
}


class ShellcodingCLI:
    """Main CLI interface"""
    
    def __init__(self):
        self.encoder = ShellcodeEncoder()
        self.compiler = ShellcodeCompiler()
        self.validator = PayloadValidator()
    
    def list_encoders(self):
        """Show available encoders"""
        print(f"\n{Fore.GREEN}Available Encoders:{Style.RESET_ALL}")
        table_data = [[k, v] for k, v in ENCODERS.items()]
        print(tabulate(table_data, headers=['Encoder', 'Description'], tablefmt='grid'))
    
    def quick_encode(self, technique, payload_file, key=None, output=None):
        """Quick encode a payload"""
        try:
            print(f"{Fore.YELLOW}[*] Encoding with {technique}...{Style.RESET_ALL}")
            
            with open(payload_file, 'r') as f:
                shellcode = f.read().strip()
            
            encoded = self.encoder.encode(technique, shellcode, key)
            
            if not output:
                output = f"{Path(payload_file).stem}_encoded_{technique}.c"
            
            with open(output, 'w') as f:
                f.write(encoded)
            
            print(f"{Fore.GREEN}[+] Encoded payload saved to: {output}{Style.RESET_ALL}")
            return output
            
        except Exception as e:
            print(f"{Fore.RED}[!] Error: {e}{Style.RESET_ALL}")
            sys.exit(1)
    
    def compile_decoder(self, encoded_payload, technique, arch='x64', platform='linux', output=None):
        """Compile encoded payload with decoder"""
        try:
            print(f"{Fore.YELLOW}[*] Compiling decoder...{Style.RESET_ALL}")
            
            with open(encoded_payload, 'r') as f:
                encoded_data = f.read()
            
            binary_path = self.compiler.compile(
                encoded_data, 
                technique, 
                arch=arch, 
                platform=platform, 
                output=output
            )
            
            print(f"{Fore.GREEN}[+] Compiled binary: {binary_path}{Style.RESET_ALL}")
            return binary_path
            
        except Exception as e:
            print(f"{Fore.RED}[!] Compilation failed: {e}{Style.RESET_ALL}")
            sys.exit(1)
    
    def test_payload(self, binary_path, verbose=False):
        """Test payload execution"""
        try:
            print(f"{Fore.YELLOW}[*] Testing payload...{Style.RESET_ALL}")
            
            result = self.validator.test(binary_path, verbose=verbose)
            
            if result['success']:
                print(f"{Fore.GREEN}[+] Payload executed successfully!{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[!] Payload execution failed{Style.RESET_ALL}")
            
            return result
            
        except Exception as e:
            print(f"{Fore.RED}[!] Test error: {e}{Style.RESET_ALL}")
            sys.exit(1)


@click.group()
def cli():
    """ShellcodingDream - Dockerized Shellcode Obfuscation Tool"""
    print(BANNER)


@cli.command()
def list():
    """List available encoders and payloads"""
    tool = ShellcodingCLI()
    tool.list_encoders()


@cli.command()
@click.option('--technique', required=True, type=click.Choice(list(ENCODERS.keys())),
              help='Encoding technique to use')
@click.option('--input', required=True, type=click.Path(exists=True),
              help='Input shellcode file (hex format)')
@click.option('--key', default=None,
              help='Encoding key (if applicable)')
@click.option('--output', default=None,
              help='Output C file path')
def encode(technique, input, key, output):
    """Encode shellcode with specified technique"""
    tool = ShellcodingCLI()
    tool.quick_encode(technique, input, key=key, output=output)


@cli.command()
@click.option('--technique', required=True, type=click.Choice(list(ENCODERS.keys())),
              help='Encoding technique')
@click.option('--input', required=True, type=click.Path(exists=True),
              help='Encoded payload file')
@click.option('--platform', type=click.Choice(['linux', 'windows']), default='linux',
              help='Target platform')
@click.option('--arch', type=click.Choice(['x86', 'x64']), default='x64',
              help='Target architecture')
@click.option('--output', default=None,
              help='Output binary path')
def compile(technique, input, platform, arch, output):
    """Compile encoded payload with decoder"""
    tool = ShellcodingCLI()
    tool.compile_decoder(input, technique, arch=arch, platform=platform, output=output)


@cli.command()
@click.option('--payload', required=True, type=click.Path(exists=True),
              help='Binary payload to test')
@click.option('--verbose', is_flag=True,
              help='Verbose output')
def test(payload, verbose):
    """Test payload execution"""
    tool = ShellcodingCLI()
    tool.test_payload(payload, verbose=verbose)


@cli.command()
@click.option('--technique', required=True, type=click.Choice(list(ENCODERS.keys())),
              help='Encoding technique')
@click.option('--input', required=True, type=click.Path(exists=True),
              help='Input shellcode file')
@click.option('--platform', type=click.Choice(['linux', 'windows']), default='linux',
              help='Target platform')
@click.option('--key', default=None,
              help='Encoding key (if needed)')
@click.option('--verbose', is_flag=True,
              help='Show detailed output')
def pipeline(technique, input, platform, key, verbose):
    """Run full pipeline: encode → compile → test"""
    tool = ShellcodingCLI()
    
    print(f"{Fore.CYAN}{'='*50}")
    print(f"Full Pipeline: {technique.upper()} → Compile → Test")
    print(f"{'='*50}{Style.RESET_ALL}\n")
    
    try:
        # Step 1: Encode
        encoded_file = tool.quick_encode(technique, input, key=key)
        
        # Step 2: Compile
        binary = tool.compile_decoder(encoded_file, technique, platform=platform)
        
        # Step 3: Test
        tool.test_payload(binary, verbose=verbose)
        
        print(f"\n{Fore.GREEN}[+] Pipeline completed successfully!{Style.RESET_ALL}")
        
    except Exception as e:
        print(f"\n{Fore.RED}[!] Pipeline failed: {e}{Style.RESET_ALL}")
        sys.exit(1)


@cli.command()
def oscp():
    """OSCP Quick Start - Fastest path for exam"""
    print(f"""
{Fore.CYAN}╔════════════════════════════════════════╗
║   OSCP Quick Start Mode                ║
║   Use these commands in exam           ║
╚════════════════════════════════════════╝{Style.RESET_ALL}

{Fore.GREEN}1. List available encoders:{Style.RESET_ALL}
   shellcoding list

{Fore.GREEN}2. Try XOR first (fastest):{Style.RESET_ALL}
   shellcoding pipeline --technique xor --input payload.hex --platform linux

{Fore.GREEN}3. If blocked, try RC4:{Style.RESET_ALL}
   shellcoding pipeline --technique rc4 --input payload.hex --platform linux

{Fore.GREEN}4. Still blocked? Try Base64:{Style.RESET_ALL}
   shellcoding pipeline --technique base64 --input payload.hex --platform linux

{Fore.YELLOW}Pro tip: Try another encoder if one fails{Style.RESET_ALL}
    """)


def main():
    """Entry point"""
    try:
        cli()
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        sys.exit(1)


if __name__ == '__main__':
    main()
