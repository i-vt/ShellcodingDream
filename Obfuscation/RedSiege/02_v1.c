#include <stdio.h>
#include <stdint.h>

// Function to encrypt shellcode using Caesar cipher (ROT13)
void caesar_cipher_encrypt(uint8_t *shellcode, size_t size) {
    for (size_t i = 0; i < size; i++) {
        shellcode[i] = (shellcode[i] + 13) % 256;  // ROT13 encryption with wrapping
    }
}

// Function to decrypt shellcode using Caesar cipher (ROT13)
void caesar_cipher_decrypt(uint8_t *shellcode, size_t size) {
    for (size_t i = 0; i < size; i++) {
        shellcode[i] = (shellcode[i] - 13 + 256) % 256;  // ROT13 decryption with wrapping
    }
}

// Function to print shellcode in hexadecimal format
void print_shellcode(uint8_t *shellcode, size_t size) {
    for (size_t i = 0; i < size; i++) {
        printf("%02X ", shellcode[i]);
    }
    printf("\n");
}

int main() {
    // Example shellcode (hex values)
    uint8_t shellcode[] = {0xFC, 0x48, 0x83, 0xE4, 0xF0};  // Example shellcode
    size_t shellcode_size = sizeof(shellcode) / sizeof(shellcode[0]);

    printf("Original shellcode:\n");
    print_shellcode(shellcode, shellcode_size);

    // Encrypt the shellcode using ROT13
    caesar_cipher_encrypt(shellcode, shellcode_size);
    printf("\nEncrypted shellcode (ROT13):\n");
    print_shellcode(shellcode, shellcode_size);

    // Decrypt the shellcode back to original
    caesar_cipher_decrypt(shellcode, shellcode_size);
    printf("\nDecrypted shellcode (back to original):\n");
    print_shellcode(shellcode, shellcode_size);

    return 0;
}

