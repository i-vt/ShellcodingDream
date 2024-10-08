#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Sample shellcode (as hex bytes)
unsigned char shellcode[] = {
    0xFC, 0x48, 0x83, 0xE4, 0xF0, 0xE8, 0x00, 0x00, 0x00, 0x00, 0x60, 0x89, 0xE5, 0x31, 0xD2, 0x64, 
    0x8B, 0x52, 0x30, 0x8B, 0x52, 0x0C, 0x8B, 0x52, 0x14, 0x8B, 0x72, 0x28, 0x0F, 0xB7, 0x4A, 0x26, 
    0x31, 0xFF, 0x31, 0xC0, 0xAC, 0x3C, 0x61, 0x7C, 0x02, 0x2C, 0x20, 0xC1, 0xCF, 0x0D, 0x01, 0xC7,
    0x49, 0x75, 0xEF, 0x52, 0x57, 0x8B, 0x52, 0x10, 0x8B, 0x42, 0x3C, 0x01, 0xD0, 0x8B, 0x40, 0x78, 
    0x85, 0xC0, 0x74, 0x4A, 0x01, 0xD0, 0x50, 0x8B, 0x48, 0x18, 0x44, 0x8B, 0x40, 0x20, 0x49, 0x01, 
    0xD0, 0xE3, 0x3C, 0x48, 0xFF, 0xD5
};

// Function to split shellcode into even and odd position arrays
void split_shellcode(unsigned char *shellcode, int size, unsigned char **evens, int *even_size, unsigned char **odds, int *odd_size) {
    // Calculate sizes for evens and odds arrays
    *even_size = (size + 1) / 2; // Even positions
    *odd_size = size / 2;        // Odd positions
    
    // Allocate memory for even and odd arrays
    *evens = (unsigned char *)malloc(*even_size * sizeof(unsigned char));
    *odds = (unsigned char *)malloc(*odd_size * sizeof(unsigned char));
    
    // Split shellcode into evens and odds arrays
    int even_idx = 0, odd_idx = 0;
    for (int i = 0; i < size; i++) {
        if (i % 2 == 0) {
            (*evens)[even_idx++] = shellcode[i];
        } else {
            (*odds)[odd_idx++] = shellcode[i];
        }
    }
}

// Function to reconstruct the shellcode from even and odd arrays
void reconstruct_shellcode(unsigned char *evens, int even_size, unsigned char *odds, int odd_size, unsigned char *reconstructed, int total_size) {
    int even_idx = 0, odd_idx = 0;
    
    for (int i = 0; i < total_size; i++) {
        if (i % 2 == 0 && even_idx < even_size) {
            reconstructed[i] = evens[even_idx++];
        } else if (i % 2 != 0 && odd_idx < odd_size) {
            reconstructed[i] = odds[odd_idx++];
        }
    }
}

int main() {
    int shellcode_size = sizeof(shellcode) / sizeof(shellcode[0]);
    
    // Arrays to hold evens and odds
    unsigned char *evens, *odds;
    int even_size, odd_size;

    // Split shellcode into evens and odds
    split_shellcode(shellcode, shellcode_size, &evens, &even_size, &odds, &odd_size);

    // Print evens and odds arrays
    printf("Evens: ");
    for (int i = 0; i < even_size; i++) {
        printf("%02X ", evens[i]);
    }
    printf("\nOdds:  ");
    for (int i = 0; i < odd_size; i++) {
        printf("%02X ", odds[i]);
    }
    printf("\n");

    // Array to hold the reconstructed shellcode
    unsigned char *reconstructed_shellcode = (unsigned char *)malloc(shellcode_size * sizeof(unsigned char));

    // Reconstruct shellcode
    reconstruct_shellcode(evens, even_size, odds, odd_size, reconstructed_shellcode, shellcode_size);

    // Print reconstructed shellcode
    printf("Reconstructed Shellcode: ");
    for (int i = 0; i < shellcode_size; i++) {
        printf("%02X ", reconstructed_shellcode[i]);
    }
    printf("\n");

    // Verify if reconstruction matches the original shellcode
    if (memcmp(shellcode, reconstructed_shellcode, shellcode_size) == 0) {
        printf("Success: The shellcode has been correctly reconstructed!\n");
    } else {
        printf("Error: The shellcode reconstruction failed!\n");
    }

    // Free allocated memory
    free(evens);
    free(odds);
    free(reconstructed_shellcode);

    return 0;
}

