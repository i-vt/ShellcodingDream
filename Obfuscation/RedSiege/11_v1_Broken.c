#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// Translation table containing 256 unique words corresponding to shellcode byte values
const char *translation_table[256] = {
    "music", "taste", "wings", "audio", "spank", "arena", "visit", "pencil",
    "zebra", "apple", "ball", "cat", "dog", "elephant", "fan", "ghost",
    // Continue adding words until all 256 slots are filled
    // For the sake of simplicity, this example uses repeated words for demonstration
};

// Example shellcode (hexadecimal format)
unsigned char shellcode[] = { 0xfc, 0x48, 0x83, 0xe4, 0xf0, 0xe8, 0xc8, 0x00 };

#define SHELLCODE_SIZE (sizeof(shellcode) / sizeof(shellcode[0]))

void encode_shellcode(unsigned char *shellcode, size_t length, char *encoded_shellcode) {
    // Encodes the shellcode using the translation table
    for (size_t i = 0; i < length; i++) {
        const char *word = translation_table[shellcode[i]];
        strcat(encoded_shellcode, word);
        if (i < length - 1) {
            strcat(encoded_shellcode, " "); // Add space between words
        }
    }
}

void decode_shellcode(const char *encoded_shellcode, unsigned char *decoded_shellcode, size_t length) {
    // Decodes the dictionary words back to the original shellcode
    char temp_encoded[1024]; // Temporary storage for manipulation
    strcpy(temp_encoded, encoded_shellcode);

    char *word = strtok(temp_encoded, " ");
    size_t index = 0;
    while (word != NULL && index < length) {
        for (int i = 0; i < 256; i++) {
            if (strcmp(word, translation_table[i]) == 0) {
                decoded_shellcode[index] = (unsigned char)i;
                break;
            }
        }
        word = strtok(NULL, " ");
        index++;
    }
}

int main() {
    char encoded_shellcode[1024] = {0}; // Buffer for encoded shellcode
    unsigned char decoded_shellcode[SHELLCODE_SIZE] = {0}; // Buffer for decoded shellcode

    // Encoding the shellcode
    encode_shellcode(shellcode, SHELLCODE_SIZE, encoded_shellcode);
    printf("Encoded Shellcode: %s\n", encoded_shellcode);

    // Decoding the shellcode
    decode_shellcode(encoded_shellcode, decoded_shellcode, SHELLCODE_SIZE);

    // Print decoded shellcode to verify it matches the original shellcode
    printf("Decoded Shellcode: ");
    for (size_t i = 0; i < SHELLCODE_SIZE; i++) {
        printf("%02x ", decoded_shellcode[i]);
    }
    printf("\n");

    // Ensure the decoded shellcode matches the original shellcode
    if (memcmp(shellcode, decoded_shellcode, SHELLCODE_SIZE) == 0) {
        printf("Decoding successful!\n");
    } else {
        printf("Decoding failed!\n");
    }

    return 0;
}

