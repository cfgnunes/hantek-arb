# ARB to CSV Converter (for Hantek oscilloscopes)

This repository provides two Python scripts for working with **ARB files** used in **Hantek oscilloscopes** to define arbitrary waveform functions. The scripts allow users to:

1. Convert ARB files to CSV format (`arb2csv.py`).
2. Convert CSV files back to ARB format (`csv2arb.py`).

## About ARB Files

ARB files are binary files used by Hantek oscilloscopes to define arbitrary waveforms. Each ARB file:

- Contains a header of 8 bytes, where the first three bytes must be `"arb"`.
- Stores 4096 signed 16-bit integer values in little-endian format that represent the waveform.
- The values are scaled to the range [-1.0, 1.0].

## Scripts Overview

### `arb2csv.py`

This script converts an ARB file into a CSV file. The CSV file contains 4096 rows, where each row represents a single floating-point value in the range [-1.0, 1.0].

### `csv2arb.py`

This script converts a CSV file back into an ARB file. The CSV must contain exactly 4096 rows with floating-point values in the range [-1.0, 1.0].

## Prerequisites

- Python 3.6 or later.

## Usage

### Converting ARB to CSV

To convert an ARB file to a CSV file, use the following command:

```bash
python arb2csv.py <file.arb>
```

For example:

```bash
python arb2csv.py sine.arb
```

This will generate a file named `sine.csv` in the same directory.

### Converting CSV to ARB

To convert a CSV file back to an ARB file, use the following command:

```bash
python csv2arb.py <file.csv>
```

For example:

```bash
python csv2arb.py sine.csv
```

This will generate a file named `sine.arb` in the same directory.

## Notes

- Ensure the CSV file contains exactly 4096 rows with valid floating-point values in the range [-1.0, 1.0].
- The scripts strictly validate file formats and will report errors if the input files are invalid.

## Contributing

If you spot a bug or want to improve the code or even improve the content, you can do the following:

- [Open an issue](https://github.com/cfgnunes/hantek-arb/issues/new)
  describing the bug or feature idea;
- Fork the project, make changes, and submit a pull request.
