import csv
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import argparse

# Define command-line arguments
parser = argparse.ArgumentParser(description='Plot spectrum data from a CSV file.')
parser.add_argument('--file', help='CSV file name', required=True)
args = parser.parse_args()

# Load and process data from the specified CSV file
def load_data(file_name):
    loaded_data = []
    with open(file_name, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            timestamp = float(row['timestamp'])

            # Process spec0 and spec1 data
            spec0 = [int(val) for val in row['spec0'][1:-1].split()]
            spec1 = [int(val) for val in row['spec1'][1:-1].split()]

            loaded_data.append({
                'timestamp': timestamp,
                'spec0': spec0,
                'spec1': spec1
            })
    return loaded_data

# Function to plot spectrum
def plot_spectrum(loaded_data, data_index):
    if data_index < 0 or data_index >= len(loaded_data):
        print("Invalid data index.")
        return

    capture_data = loaded_data[data_index]
    timestamp = capture_data['timestamp']
    spec0_data = capture_data['spec0']
    spec1_data = capture_data['spec1']

    fig0, ax0 = plt.subplots()
    ax0.plot(np.linspace(-256/2, 256/2-1, 256) * 125/256, 10 * np.log10(spec0_data[:256], 'b-'))
    ax0.set(xlabel='freq (MHz)', ylabel='power(dB)', title=f'Channel 0 Spectrum - {datetime.fromtimestamp(timestamp)}')
    ax0.set_xlim(0, 62.5)
    ax0.set_ylim(20, 100)
    ax0.grid()

    fig1, ax1 = plt.subplots()
    ax1.plot(np.linspace(-256/2, 256/2-1, 256) * 125/256, 10 * np.log10(spec1_data[:256], 'b-'))
    ax1.set(xlabel='freq (MHz)', ylabel='power(dB)', title=f'Channel 1 Spectrum - {datetime.fromtimestamp(timestamp)}')
    ax1.set_xlim(0, 62.5)
    ax1.set_ylim(20, 100)
    ax1.grid()

    plt.show()

# Input the data index from the user
data_index = int(input("Enter the data index: "))

# Load and process data from the specified CSV file
csv_file_name = args.file
loaded_data = load_data(csv_file_name)

# Plot the spectrum for the specified data index
plot_spectrum(loaded_data, data_index)
