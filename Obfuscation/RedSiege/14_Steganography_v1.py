from PIL import Image

def encode_shellcode_in_image(image_path, shellcode, output_path):
    # Open the image
    img = Image.open(image_path)
    pixels = img.load()
    
    # Convert shellcode to binary
    shellcode_bits = ''.join(format(byte, '08b') for byte in shellcode)
    
    # Modify the image pixels to hide the shellcode
    width, height = img.size
    index = 0
    for x in range(width):
        for y in range(height):
            if index < len(shellcode_bits):
                r, g, b = pixels[x, y]
                # Modify LSB of red channel
                r = (r & ~1) | int(shellcode_bits[index])
                pixels[x, y] = (r, g, b)
                index += 1
    
    # Save the modified image
    img.save(output_path)
    print(f"Shellcode encoded in image and saved to {output_path}")

def decode_shellcode_from_image(image_path, shellcode_length):
    img = Image.open(image_path)
    pixels = img.load()
    
    # Extract LSBs to reconstruct the shellcode
    width, height = img.size
    shellcode_bits = ''
    for x in range(width):
        for y in range(height):
            if len(shellcode_bits) < shellcode_length * 8:
                r, g, b = pixels[x, y]
                shellcode_bits += str(r & 1)
    
    # Convert bits back to bytes
    shellcode = bytes(int(shellcode_bits[i:i+8], 2) for i in range(0, len(shellcode_bits), 8))
    return shellcode

# Example usage
if __name__ == "__main__":
    # Define the shellcode you want to hide
    shellcode = b"\x48\x31\xc0\x48\x89\xc2\x48\x89\xc6"  # Example shellcode
    
    # Encode the shellcode into the image
    encode_shellcode_in_image("input_image.png", shellcode, "output_image.png")
    
    # Decode the shellcode from the image
    decoded_shellcode = decode_shellcode_from_image("output_image.png", len(shellcode))
    print(f"Decoded shellcode: {decoded_shellcode}")

