#!/usr/bin/env python3

import struct
import csv
import sys
import os


def main():
    # Check if the filename was provided as a command-line argument.
    if len(sys.argv) != 2:
        print("Usage: python arb2csv.py <file.arb>")
        sys.exit(1)

    # Get the input file name from the arguments.
    input_file = sys.argv[1]

    # Check if the file exists.
    if not os.path.isfile(input_file):
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)

    # Generate the output file name (replace extension with .csv).
    output_file = os.path.splitext(input_file)[0] + ".csv"

    # Open the binary file for reading.
    with open(input_file, "rb") as binary_file:
        # Read and verify the 8-byte header.
        header = binary_file.read(8)
        if header[:3] != b"arb":
            print("Error: This is not a ARB file.")
            sys.exit(1)

        # Read the remaining data (4096 values, each 2 bytes).
        binary_data = binary_file.read(4096 * 2)

    # Convert binary data into floating-point values.
    values = []
    for i in range(0, len(binary_data), 2):
        # Interpret each pair of bytes as a signed 16-bit
        # integer (little-endian).
        value = struct.unpack("<h", binary_data[i:i+2])[0]
        # Map the signed value to the range.
        value = value / (4095.0 / 2)
        # Scale to [-1.0, 1.0].
        value = value - 1.0
        values.append(value)

    # Write the values to a CSV file.
    with open(output_file, "w", encoding="utf-8", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        # Write the values.
        for value in values:
            csv_writer.writerow([f"{value:.8f}"])

    print(f"Conversion complete. CSV file saved as '{output_file}'.")


if __name__ == '__main__':
    main()
