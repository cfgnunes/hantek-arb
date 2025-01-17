#!/usr/bin/env python3

import csv
import os
import struct
import sys

NUM_VALUES = 4096


def main():
    # Check if at least one argument (input file) is provided.
    if len(sys.argv) < 2:
        print("Usage: python csv2arb.py <file.csv> [output.arb]")
        sys.exit(1)

    # Get the input file name from the arguments.
    input_file = sys.argv[1]

    # Check if the file exists.
    if not os.path.isfile(input_file):
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)

    # Check if an output file name was provided.
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    else:
        output_file = os.path.splitext(input_file)[0] + ".arb"

    # Read values from CSV.
    values = read_csv(input_file)

    # Write values to ARB.
    write_arb(output_file, values)


def read_csv(filname):
    values = []
    with open(filname, "r",  encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            if len(row) != 1:
                print("Error: CSV file should contain one value per row.")
                sys.exit(1)
            try:
                # Parse the floating-point value.
                float_value = float(row[0])
                # Assuming one column of float values.
                values.append(float_value)
            except ValueError:
                print(f"Error: Invalid value '{row[0]}' in the CSV file.")
                sys.exit(1)

    # Check if the CSV file has exactly NUM_VALUES values.
    if len(values) != NUM_VALUES:
        print(
            f"Error: CSV file must contain exactly {NUM_VALUES} values, "
            f"but {len(values)} values were found."
        )
        sys.exit(1)
    return values


def write_arb(output_file, values):
    # Convert the values to signed 16-bit integers.
    binary_data = b""
    for value in values:
        # Reverse the scaling: map [-1.0, 1.0] back to 16-bit integer.
        value = (value + 1.0) * ((NUM_VALUES - 1) / 2.0)
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


if __name__ == "__main__":
    main()
