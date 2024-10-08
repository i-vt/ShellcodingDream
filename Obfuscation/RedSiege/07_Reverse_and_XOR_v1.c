#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main() {
    unsigned char shellcode[] = {0xFC, 0x48, 0x83, 0xE4, 0xFF, 0xD5};
    int shellcode_size = sizeof(shellcode);
    
    // Generate a random XOR key
    srand(time(NULL));
    unsigned char xor_key = rand() % 256;

    printf("XOR Key: %02X\n", xor_key);
    
    printf("Reversed XOR-Encoded Shellcode: ");
    for (int i = shellcode_size - 1; i >= 0; i--) {
        printf("%02X ", shellcode[i] ^ xor_key);
    }
    printf("\n");

    return 0;
}

