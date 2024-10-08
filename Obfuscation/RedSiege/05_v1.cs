using System;
using System.Text;

class Program
{
    static void Main()
    {
        // Example Base64 encoded shellcode (replace this with real encoded shellcode)
        string base64Shellcode = "/EID...Q=="; // truncated example from the talk

        // Step 1: Decode the Base64 encoded shellcode to a byte array
        byte[] shellcodeBytes = Convert.FromBase64String(base64Shellcode);
        
        // Step 2: Print the decoded shellcode as hexadecimal values
        Console.WriteLine("Decoded Shellcode (Hex):");
        foreach (byte b in shellcodeBytes)
        {
            Console.Write($"{b:X2} "); // Print each byte in hex
        }
        Console.WriteLine();

        // Step 3: Emulate executing the shellcode (simplified for the sake of demo)
        // In real scenarios, you would allocate memory and execute, but that's beyond
        // the scope of safe, legal, and ethical code here.
        Console.WriteLine("Shellcode decoded into byte array successfully, ready for execution.");
    }
}
// Encode shellcode (byte array) into Base64 format
//byte[] shellcode = { 0xFC, 0x48, 0x83, 0xE4, 0xF0, 0xFF, 0xD5 }; // Example shellcode
// string encodedShellcode = Convert.ToBase64String(shellcode);
// Console.WriteLine("Encoded Shellcode (Base64): " + encodedShellcode);

