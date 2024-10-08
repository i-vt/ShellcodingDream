import random
import sys

# Function to read the shellcode from a binary file
def read_shellcode(filename):
    with open(filename, 'rb') as f:
        return list(f.read())

# Function to generate Jigsaw-encoded shellcode
def generate_jigsaw(shellcode):
    # Get the length of the shellcode
    shellcode_length = len(shellcode)

    # Create a list of positions corresponding to each byte in the shellcode
    raw_positions = list(range(shellcode_length))

    # Shuffle the positions to randomize the order
    random.shuffle(raw_positions)

    # Create the jigsaw-encoded shellcode by reordering the bytes
    jigsaw = [shellcode[i] for i in raw_positions]

    # Return the shuffled positions and the jigsaw shellcode
    return raw_positions, jigsaw

# Function to save the scrambled shellcode and positions to a file
def save_jigsaw_to_file(positions, jigsaw, output_file):
    with open(output_file, 'w') as f:
        # Writing the scrambled shellcode
        f.write("Jigsaw (scrambled shellcode):\n")
        f.write(', '.join(hex(byte) for byte in jigsaw) + '\n')

        # Writing the shuffled positions
        f.write("\nPositions (scrambled indices):\n")
        f.write(', '.join(str(pos) for pos in positions) + '\n')

# Function to reconstruct the original shellcode using the positions and jigsaw list
def reconstruct_shellcode(positions, jigsaw):
    shellcode_length = len(positions)
    reconstructed_shellcode = [0] * shellcode_length

    # Rebuild the shellcode by placing each byte at its original position
    for i, pos in enumerate(positions):
        reconstructed_shellcode[pos] = jigsaw[i]

    return reconstructed_shellcode

# Main function to tie everything together
def main(input_file, output_file):
    # Read the shellcode from the input binary file
    shellcode = read_shellcode(input_file)

    # Generate the jigsaw scrambled shellcode and positions
    positions, jigsaw = generate_jigsaw(shellcode)

    # Save the scrambled shellcode and positions to an output file
    save_jigsaw_to_file(positions, jigsaw, output_file)

    # Reconstruct the original shellcode
    reconstructed_shellcode = reconstruct_shellcode(positions, jigsaw)

    # Print the original and reconstructed shellcodes for comparison
    print("Original Shellcode:")
    print(', '.join(hex(byte) for byte in shellcode))
    print("\nReconstructed Shellcode:")
    print(', '.join(hex(byte) for byte in reconstructed_shellcode))

    # Check if the reconstruction was successful
    if shellcode == reconstructed_shellcode:
        print("\nReconstruction successful!")
    else:
        print("\nReconstruction failed!")

# Run the script
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <input_shellcode_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    main(input_file, output_file)

