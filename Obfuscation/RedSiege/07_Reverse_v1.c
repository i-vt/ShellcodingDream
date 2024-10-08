#include <stdio.h>

int main() {
    unsigned char shellcode[] = {0xFC, 0x48, 0x83, 0xE4, 0xFF, 0xD5};
    int shellcode_size = sizeof(shellcode);
    
    printf("Reversed Shellcode: ");
    for (int i = shellcode_size - 1; i >= 0; i--) {
        printf("%02X ", shellcode[i]);
    }
    printf("\n");

    return 0;
}

