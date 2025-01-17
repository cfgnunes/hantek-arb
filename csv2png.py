#!/usr/bin/env python3


import csv
import os
import sys
import numpy as np
import matplotlib.pyplot as plt

NUM_VALUES = 4096


def main():
    # Check if at least one argument (input file) is provided.
    if len(sys.argv) < 2:
        print("Usage: python csv2png.py <file.csv> [output.png]")
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
        output_file = os.path.splitext(input_file)[0] + ".png"

    # Read values from CSV.
    values = read_csv(input_file)

    # Plot values to PNG.
    plot_waveform(values, output_file)


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


def plot_waveform(values, output_file):
    # Generate percentage values for the x-axis (0% to 100%).
    x_percent = np.linspace(0, 100, len(values))

    # Create a plot with black background for the figure.
    plt.figure(figsize=(8, 5), facecolor="black")

    # Get current axes and set the background color to black.
    ax = plt.gca()
    ax.set_facecolor("black")

    # Set title and labels in white to contrast with black background.
    plt.xlabel("Period (%)", color="white")
    plt.ylabel("Amplitude", color="white")

    # Set axis limits.
    plt.xlim(0, 100)
    plt.ylim(-1.05, 1.05)
    # Set axis ticks.
    plt.xticks([0, 25, 50, 75, 100],
               ["0%", "25%", "50%", "75%", "100%"], color="white")
    plt.yticks([-1, -0.5, 0, 0.5, 1], color="white")

    # Add regular grid lines.
    plt.grid(True, which="both", color="gray", linestyle="dotted", linewidth=1)

    # Add thicker center grid lines for both axes.
    ax.axhline(0, color="gray", linewidth=1.5, linestyle="-")
    ax.axvline(50, color="gray", linewidth=1.5, linestyle="-")

    # Add a white box around the plot (spines of the axes).
    for spine in ["top", "bottom", "left", "right"]:
        ax.spines[spine].set_edgecolor("white")
        ax.spines[spine].set_linewidth(1)

    # Plot the waveform in yellow color.
    plt.plot(x_percent, values, color="yellow")

    # Save the plot as a PNG file.
    plt.savefig(output_file, format="png", bbox_inches="tight")

    print(f"Waveform plot saved as '{output_file}'.")


if __name__ == "__main__":
    main()
