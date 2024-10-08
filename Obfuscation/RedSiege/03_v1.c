//gcc 03_v1.c -o 03_v1 -lcrypto -lssl
//sudo apt-get install libssl-dev

#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <openssl/evp.h>
#include <openssl/rand.h>

// Example shellcode (replace with actual shellcode as needed)
unsigned char shellcode[] = { 0xfc, 0x48, 0x83, 0xe4, 0xf0, 0xe8, 0xc0, 0x00, 0x00, 0x00 };

// AES Encryption using EVP
int aes_encrypt(unsigned char *plaintext, int plaintext_len, unsigned char *key, unsigned char *iv, unsigned char *ciphertext) {
    EVP_CIPHER_CTX *ctx;
    int len;
    int ciphertext_len;

    // Create and initialize the context
    if(!(ctx = EVP_CIPHER_CTX_new())) {
        fprintf(stderr, "Failed to create context for AES encryption\n");
        return -1;
    }

    // Initialize the encryption operation with AES-128-CBC
    if(1 != EVP_EncryptInit_ex(ctx, EVP_aes_128_cbc(), NULL, key, iv)) {
        fprintf(stderr, "Failed to initialize AES encryption\n");
        EVP_CIPHER_CTX_free(ctx);
        return -1;
    }

    // Perform the encryption
    if(1 != EVP_EncryptUpdate(ctx, ciphertext, &len, plaintext, plaintext_len)) {
        fprintf(stderr, "Failed to update AES encryption\n");
        EVP_CIPHER_CTX_free(ctx);
        return -1;
    }
    ciphertext_len = len;

    // Finalize the encryption
    if(1 != EVP_EncryptFinal_ex(ctx, ciphertext + len, &len)) {
        fprintf(stderr, "Failed to finalize AES encryption\n");
        EVP_CIPHER_CTX_free(ctx);
        return -1;
    }
    ciphertext_len += len;

    // Clean up
    EVP_CIPHER_CTX_free(ctx);

    return ciphertext_len;
}

// AES Decryption using EVP
int aes_decrypt(unsigned char *ciphertext, int ciphertext_len, unsigned char *key, unsigned char *iv, unsigned char *plaintext) {
    EVP_CIPHER_CTX *ctx;
    int len;
    int plaintext_len;

    // Create and initialize the context
    if(!(ctx = EVP_CIPHER_CTX_new())) {
        fprintf(stderr, "Failed to create context for AES decryption\n");
        return -1;
    }

    // Initialize the decryption operation with AES-128-CBC
    if(1 != EVP_DecryptInit_ex(ctx, EVP_aes_128_cbc(), NULL, key, iv)) {
        fprintf(stderr, "Failed to initialize AES decryption\n");
        EVP_CIPHER_CTX_free(ctx);
        return -1;
    }

    // Perform the decryption
    if(1 != EVP_DecryptUpdate(ctx, plaintext, &len, ciphertext, ciphertext_len)) {
        fprintf(stderr, "Failed to update AES decryption\n");
        EVP_CIPHER_CTX_free(ctx);
        return -1;
    }
    plaintext_len = len;

    // Finalize the decryption
    if(1 != EVP_DecryptFinal_ex(ctx, plaintext + len, &len)) {
        fprintf(stderr, "Failed to finalize AES decryption\n");
        EVP_CIPHER_CTX_free(ctx);
        return -1;
    }
    plaintext_len += len;

    // Clean up
    EVP_CIPHER_CTX_free(ctx);

    return plaintext_len;
}

int main(int argc, char* argv[]) {
    // Example AES key and IV (should be replaced with proper key/IV handling)
    unsigned char key[16] = "0123456789abcdef";  // 16-byte key for AES-128
    unsigned char iv[16];  // 16-byte IV for AES

    // Generate a random IV
    if (!RAND_bytes(iv, sizeof(iv))) {
        fprintf(stderr, "Failed to generate random IV\n");
        return 1;
    }

    unsigned char encrypted_shellcode[128];
    unsigned char decrypted_shellcode[128];
    int encrypted_len, decrypted_len;

    // Encrypt the shellcode
    encrypted_len = aes_encrypt(shellcode, sizeof(shellcode), key, iv, encrypted_shellcode);
    if (encrypted_len == -1) {
        fprintf(stderr, "AES encryption failed\n");
        return 1;
    }

    printf("Encrypted Shellcode: ");
    for (int i = 0; i < encrypted_len; i++) {
        printf("%02x ", encrypted_shellcode[i]);
    }
    printf("\n");

    // Decrypt the shellcode
    decrypted_len = aes_decrypt(encrypted_shellcode, encrypted_len, key, iv, decrypted_shellcode);
    if (decrypted_len == -1) {
        fprintf(stderr, "AES decryption failed\n");
        return 1;
    }

    printf("Decrypted Shellcode: ");
    for (int i = 0; i < decrypted_len; i++) {
        printf("%02x ", decrypted_shellcode[i]);
    }
    printf("\n");

    return 0;
}

