#!/usr/bin/env python3

import struct
import csv
import sys
import os


def main():
    # Check if the filename was provided as a command-line argument.
    if len(sys.argv) != 2:
        print("Usage: python csv2arb.py <file.csv>")
        sys.exit(1)

    # Get the input file name from the arguments
    input_file = sys.argv[1]

    # Check if the file exists
    if not os.path.isfile(input_file):
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)

    # Generate the output file name (replace extension with .arb).
    output_file = os.path.splitext(input_file)[0] + ".arb"

    # Read the CSV file.
    values = []
    with open(input_file, "r", encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            if len(row) != 1:
                print("Error: CSV file should contain one value per row.")
                sys.exit(1)
            try:
                # Parse the floating-point value.
                float_value = float(row[0])
                # Ensure the value is in the range [-1.0, 1.0].
                if not -1.0 <= float_value <= 1.0:
                    print(
                        f"Error: Value '{float_value}' "
                        "is out of range [-1.0, 1.0]."
                    )
                    sys.exit(1)
                values.append(float_value)
            except ValueError:
                print(f"Error: Invalid value '{row[0]}' in the CSV file.")
                sys.exit(1)

    # Check that we have exactly 4096 values
    if len(values) != 4096:
        print(
            "Error: CSV file must contain exactly 4096 values, "
            f"but {len(values)} were found."
        )
        sys.exit(1)

    # Convert the values to signed 16-bit integers.
    binary_data = b""
    for value in values:
        # Reverse the scaling: map [-1.0, 1.0] back to 16-bit integer.
        value = (value + 1.0) * (4095.0 / 2)
        int_value = int(round(value))
        # Pack as little-endian signed 16-bit integer.
        binary_data += struct.pack("<h", int_value)

    # Write the ARB binary file.
    with open(output_file, "wb") as binary_file:
        # Write the 8-byte header.
        binary_file.write(b"arb" + b"\x00\x00\x11\x00\x00")
        # Write the binary data.
        binary_file.write(binary_data)

    print(f"Conversion complete. ARB file saved as '{output_file}'.")


if __name__ == '__main__':
    main()
