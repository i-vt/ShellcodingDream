# Sample shellcode (as hex bytes)
shellcode = [0xFC, 0x48, 0x83, 0xE4, 0xF0, 0xE8, 0x00, 0x00, 0x00, 0x00, 0x60, 0x89, 0xE5, 0x31, 0xD2, 0x64, 0x8B, 0x52, 0x30, 0x8B, 0x52, 0x0C, 0x8B, 0x52, 0x14, 0x8B, 0x72, 0x28, 0x0F, 0xB7, 0x4A, 0x26, 0x31, 0xFF, 0x31, 0xC0, 0xAC, 0x3C, 0x61, 0x7C, 0x02, 0x2C, 0x20, 0xC1, 0xCF, 0x0D, 0x01, 0xC7, 0x49, 0x75, 0xEF, 0x52, 0x57, 0x8B, 0x52, 0x10, 0x8B, 0x42, 0x3C, 0x01, 0xD0, 0x8B, 0x40, 0x78, 0x85, 0xC0, 0x74, 0x4A, 0x01, 0xD0, 0x50, 0x8B, 0x48, 0x18, 0x44, 0x8B, 0x40, 0x20, 0x49, 0x01, 0xD0, 0xE3, 0x3C, 0x48, 0xFF, 0xD5]  # Shortened for illustration

# Function to split shellcode into even and odd position arrays
def split_shellcode(shellcode):
    evens = []
    odds = []
    for i in range(len(shellcode)):
        if i % 2 == 0:
            evens.append(shellcode[i])
        else:
            odds.append(shellcode[i])
    return evens, odds

# Function to reconstruct the shellcode from even and odd arrays
def reconstruct_shellcode(evens, odds):
    reconstructed_shellcode = []
    even_idx = 0
    odd_idx = 0
    
    # Iterate and combine the evens and odds arrays
    for i in range(len(evens) + len(odds)):
        if i % 2 == 0:
            if even_idx < len(evens):
                reconstructed_shellcode.append(evens[even_idx])
                even_idx += 1
        else:
            if odd_idx < len(odds):
                reconstructed_shellcode.append(odds[odd_idx])
                odd_idx += 1
                
    return reconstructed_shellcode

# Split the shellcode into evens and odds
evens, odds = split_shellcode(shellcode)

# Print the split arrays
print("Evens: ", evens)
print("Odds:  ", odds)

# Reconstruct the shellcode from the split arrays
reconstructed_shellcode = reconstruct_shellcode(evens, odds)

# Verify the reconstruction
print("Original Shellcode:   ", shellcode)
print("Reconstructed Shellcode:", reconstructed_shellcode)

# Check if the reconstructed shellcode matches the original
if shellcode == reconstructed_shellcode:
    print("Success: The shellcode has been correctly reconstructed!")
else:
    print("Error: The shellcode reconstruction failed!")

