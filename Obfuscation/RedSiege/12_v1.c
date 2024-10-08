#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// Example shellcode (this would normally be read from a file)
unsigned char shellcode[] = {
    0xfc, 0x48, 0x83, 0xe4, 0xf0, 0xe8, 0xc0, 0x00,
    0x00, 0x00, 0x41, 0x51, 0x41, 0x50, 0x52, 0x51,
    0x56, 0x48, 0x31, 0xd2, 0x65, 0x48, 0x8b, 0x52,
    0x60, 0x48, 0x8b, 0x52, 0x18, 0x48, 0x8b, 0x52
};

#define SHELLCODE_SIZE sizeof(shellcode) / sizeof(shellcode[0])

// Function to generate a shuffled list of positions
void generate_shuffled_positions(int *positions, int size) {
    for (int i = 0; i < size; i++) {
        positions[i] = i;
    }

    // Shuffle the positions array using Fisher-Yates shuffle algorithm
    for (int i = size - 1; i > 0; i--) {
        int j = rand() % (i + 1);
        int temp = positions[i];
        positions[i] = positions[j];
        positions[j] = temp;
    }
}

// Function to scramble the shellcode using the shuffled positions
void scramble_shellcode(unsigned char *jigsaw, int *positions, unsigned char *original, int size) {
    for (int i = 0; i < size; i++) {
        jigsaw[i] = original[positions[i]];
    }
}

// Function to reconstruct the original shellcode using the scrambled positions
void reconstruct_shellcode(unsigned char *reconstructed, int *positions, unsigned char *jigsaw, int size) {
    for (int i = 0; i < size; i++) {
        reconstructed[positions[i]] = jigsaw[i];
    }
}

// Function to print shellcode bytes in hex
void print_shellcode(unsigned char *code, int size) {
    for (int i = 0; i < size; i++) {
        printf("0x%02x, ", code[i]);
        if ((i + 1) % 8 == 0) {
            printf("\n");
        }
    }
    printf("\n");
}

int main() {
    srand(time(NULL)); // Seed the random number generator

    int positions[SHELLCODE_SIZE];
    unsigned char jigsaw[SHELLCODE_SIZE];
    unsigned char reconstructed[SHELLCODE_SIZE];

    // Generate shuffled positions
    generate_shuffled_positions(positions, SHELLCODE_SIZE);

    // Scramble the shellcode using the shuffled positions
    scramble_shellcode(jigsaw, positions, shellcode, SHELLCODE_SIZE);

    // Print original shellcode
    printf("Original Shellcode:\n");
    print_shellcode(shellcode, SHELLCODE_SIZE);

    // Print scrambled shellcode
    printf("\nScrambled Shellcode (Jigsaw):\n");
    print_shellcode(jigsaw, SHELLCODE_SIZE);

    // Reconstruct the original shellcode from the jigsaw array
    reconstruct_shellcode(reconstructed, positions, jigsaw, SHELLCODE_SIZE);

    // Print reconstructed shellcode
    printf("\nReconstructed Shellcode:\n");
    print_shellcode(reconstructed, SHELLCODE_SIZE);

    // Verify if the reconstruction was successful
    int success = 1;
    for (int i = 0; i < SHELLCODE_SIZE; i++) {
        if (shellcode[i] != reconstructed[i]) {
            success = 0;
            break;
        }
    }

    if (success) {
        printf("\nReconstruction successful!\n");
    } else {
        printf("\nReconstruction failed!\n");
    }

    return 0;
}

