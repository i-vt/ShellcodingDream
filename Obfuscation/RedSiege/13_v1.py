def encode_shellcode(shellcode):
    # Convert the shellcode (hex string) into byte array
    raw_sc = bytearray.fromhex(shellcode)

    # Initialize the offset array and set the first byte as the previous byte
    offset_array = []
    previous_byte = raw_sc[0]

    # Loop through the shellcode starting from the second byte
    for i in range(1, len(raw_sc)):
        current_byte = raw_sc[i]
        # Calculate the delta (difference) between current and previous byte
        delta = current_byte - previous_byte
        if delta < 0:
            # Adjust if the difference is negative
            delta += 256
        # Append the delta to the offset array
        offset_array.append(delta)
        # Set the previous byte to the current byte for the next iteration
        previous_byte = current_byte

    return raw_sc[0], offset_array  # Return the first byte and the offset array


def decode_shellcode(first_byte, offset_array):
    # Initialize the shellcode array with the first byte
    shellcode = [first_byte]

    # Reconstruct the shellcode from the offset array
    for delta in offset_array:
        current_byte = (shellcode[-1] + delta) % 256  # Add delta to previous byte and mod 256
        shellcode.append(current_byte)

    return bytearray(shellcode)  # Return the reconstructed shellcode as a byte array


# Example shellcode (in hex format)
example_shellcode = "fc4883e4f0e8c0"  # Replace with actual shellcode

# Encode the shellcode (generate delta array)
first_byte, offset_array = encode_shellcode(example_shellcode)
print(f"First Byte: {hex(first_byte)}")
print(f"Offset Array: {offset_array}")

# Decode the shellcode (reconstruct it from the delta array)
reconstructed_shellcode = decode_shellcode(first_byte, offset_array)
print(f"Reconstructed Shellcode: {reconstructed_shellcode.hex()}")

# Comparison to check if the original and reconstructed shellcode are the same
original_shellcode = bytearray.fromhex(example_shellcode)
if reconstructed_shellcode == original_shellcode:
    print("Shellcode successfully reconstructed!")
else:
    print("Shellcode reconstruction failed.")

