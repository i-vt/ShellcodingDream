#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

// Function to encode shellcode using delta encoding
void encode_shellcode(uint8_t *shellcode, int length, uint8_t *first_byte, int8_t *offset_array) {
    // Set the first byte as the previous byte
    *first_byte = shellcode[0];
    uint8_t previous_byte = shellcode[0];

    // Loop through the shellcode starting from the second byte
    for (int i = 1; i < length; i++) {
        uint8_t current_byte = shellcode[i];
        int8_t delta = current_byte - previous_byte;

        // If the result is negative, adjust it
        if (delta < 0) {
            delta += 256;
        }

        // Store the delta in the offset array
        offset_array[i - 1] = delta;
        previous_byte = current_byte;
    }
}

// Function to decode the shellcode from the delta encoding
void decode_shellcode(uint8_t first_byte, int8_t *offset_array, int length, uint8_t *reconstructed_shellcode) {
    // Set the first byte of the reconstructed shellcode
    reconstructed_shellcode[0] = first_byte;

    // Reconstruct the shellcode using the offset array
    for (int i = 1; i < length; i++) {
        reconstructed_shellcode[i] = (reconstructed_shellcode[i - 1] + offset_array[i - 1]) % 256;
    }
}

// Helper function to print byte arrays in hex
void print_shellcode(uint8_t *shellcode, int length) {
    for (int i = 0; i < length; i++) {
        printf("%02x", shellcode[i]);
    }
    printf("\n");
}

int main() {
    // Example shellcode (in hex format)
    uint8_t shellcode[] = {0xfc, 0x48, 0x83, 0xe4, 0xf0, 0xe8, 0xc0};  // Replace with actual shellcode
    int length = sizeof(shellcode) / sizeof(shellcode[0]);

    // Arrays to store encoded data
    uint8_t first_byte;
    int8_t offset_array[length - 1];

    // Encode the shellcode
    encode_shellcode(shellcode, length, &first_byte, offset_array);
    printf("First Byte: %02x\n", first_byte);
    printf("Offset Array: ");
    for (int i = 0; i < length - 1; i++) {
        printf("%02x ", offset_array[i] & 0xff);  // Displaying as unsigned hex
    }
    printf("\n");

    // Array to store the reconstructed shellcode
    uint8_t reconstructed_shellcode[length];

    // Decode the shellcode
    decode_shellcode(first_byte, offset_array, length, reconstructed_shellcode);

    // Print the reconstructed shellcode
    printf("Reconstructed Shellcode: ");
    print_shellcode(reconstructed_shellcode, length);

    // Compare original and reconstructed shellcode
    int success = 1;
    for (int i = 0; i < length; i++) {
        if (shellcode[i] != reconstructed_shellcode[i]) {
            success = 0;
            break;
        }
    }

    if (success) {
        printf("Shellcode successfully reconstructed!\n");
    } else {
        printf("Shellcode reconstruction failed.\n");
    }

    return 0;
}

