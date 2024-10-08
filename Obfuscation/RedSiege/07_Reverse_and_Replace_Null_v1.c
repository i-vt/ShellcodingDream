#include <stdio.h>
#include <string.h>

int main() {
    unsigned char shellcode[] = {0xFC, 0x48, 0x83, 0xE4, 0x00, 0xFF, 0xD5};
    int shellcode_size = sizeof(shellcode);
    char hex_string[128] = {0};
    
    // Convert shellcode to hex string and reverse it
    for (int i = shellcode_size - 1; i >= 0; i--) {
        char tmp[4];
        sprintf(tmp, "%02X", shellcode[i]);
        
        // Replace null byte with 'Z'
        if (strcmp(tmp, "00") == 0) {
            strcat(hex_string, "Z");
        } else {
            strcat(hex_string, tmp);
        }
    }

    printf("Reversed Hex String with Nulls Replaced: %s\n", hex_string);

    return 0;
}

