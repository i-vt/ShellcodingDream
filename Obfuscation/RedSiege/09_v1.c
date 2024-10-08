#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <arpa/inet.h>

// Function to pad shellcode with 0x90 (NOP) to match chunk size
unsigned char* pad_shellcode(unsigned char* shellcode, size_t shellcode_len, size_t chunk_size, size_t* padded_size) {
    size_t padding_len = chunk_size - (shellcode_len % chunk_size);
    *padded_size = shellcode_len + padding_len;
    
    unsigned char* padded_shellcode = malloc(*padded_size);
    if (padded_shellcode == NULL) {
        fprintf(stderr, "Memory allocation error\n");
        exit(1);
    }

    memcpy(padded_shellcode, shellcode, shellcode_len);
    memset(padded_shellcode + shellcode_len, 0x90, padding_len); // Padding with NOPs (0x90)

    return padded_shellcode;
}

// Convert 4-byte chunk of shellcode to IPv4 string
void convert_to_ipv4(unsigned char* chunk) {
    struct in_addr addr;
    memcpy(&addr, chunk, 4);
    printf("%s\n", inet_ntoa(addr)); // Convert binary to dotted-quad format
}

// Convert 16-byte chunk of shellcode to IPv6 string
void convert_to_ipv6(unsigned char* chunk) {
    char ipv6_str[INET6_ADDRSTRLEN];
    struct in6_addr addr;
    memcpy(&addr, chunk, 16);
    inet_ntop(AF_INET6, &addr, ipv6_str, INET6_ADDRSTRLEN);
    printf("%s\n", ipv6_str); // Convert binary to IPv6 string format
}

// Function to convert shellcode to IP addresses based on version
void shellcode_to_ip(unsigned char* shellcode, size_t shellcode_len, int version) {
    size_t chunk_size = (version == 4) ? 4 : 16;
    size_t padded_size;
    
    // Pad shellcode to match chunk size
    unsigned char* padded_shellcode = pad_shellcode(shellcode, shellcode_len, chunk_size, &padded_size);

    // Process the shellcode in chunks
    for (size_t i = 0; i < padded_size; i += chunk_size) {
        if (version == 4) {
            convert_to_ipv4(padded_shellcode + i);
        } else if (version == 6) {
            convert_to_ipv6(padded_shellcode + i);
        }
    }

    free(padded_shellcode);
}

int main() {
    // Example shellcode (replace with actual shellcode bytes)
    unsigned char shellcode[] = {0x31, 0xc0, 0xb0, 0x01, 0x31, 0xdb, 0xcd, 0x80};
    size_t shellcode_len = sizeof(shellcode);

    // Choose IP version (4 for IPv4, 6 for IPv6)
    int ip_version = 4; // Change to 6 for IPv6

    // Convert shellcode to IP addresses
    shellcode_to_ip(shellcode, shellcode_len, ip_version);

    return 0;
}

