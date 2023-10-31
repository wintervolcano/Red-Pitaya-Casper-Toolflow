import casperfpga
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import argparse
import time
from datetime import datetime
import csv
from collections import deque
import warnings
import threading 
data_lock = threading.Lock()
warnings.filterwarnings("ignore")

#Help text
parser = argparse.ArgumentParser()
parser.add_argument("-a", "--accums", help="Number of accumulations", default=5)
parser.add_argument("-ch1", "--chan1", help="starting power calculation channel", default=0)
parser.add_argument("-ch2", "--chan2", help="ending power calculation channel", default=50)
args = parser.parse_args()

#Connecting RP and uploading fpg file
fpga = casperfpga.CasperFpga('rp-f05ad8.local')
fpga.upload_to_ram_and_program('tut_spec.fpg')

#Input parameters
acc_len = int(args.accums) 
ch1 = int(args.chan1)
ch2 = int(args.chan2) 
fft_len = 256
snap_cyc = 10

#configuring the fpga design
fpga.write_int('acc_len', acc_len)
fpga.write_int('snap_gap', snap_cyc)

# Initialize variables for total power plot
total_power1 = deque(maxlen=50)
time_values1 = deque(maxlen=50)
total_power2 = deque(maxlen=50)
time_values2 = deque(maxlen=50)

# Create a list to store data and timestamps
all_data = []  

#initialize data and plot for the dynamic power vs frequency plot
n_time_points = 20  # Number of time points
n_freq_points = 128 # Number of frequency points

# Initialize power_data1 and power_data2 as deques
#This is for efficiency and also for the plot to continue
power_data1 = deque(maxlen=n_time_points)
power_data2 = deque(maxlen=n_time_points)
power_data1 = np.zeros((n_time_points, n_freq_points))
power_data2 = np.zeros((n_time_points, n_freq_points))

cmap = plt.get_cmap('viridis')
frame_index = [0] #initial frame. This will be updates every time inside the update_plot() function

current_time = datetime.now().strftime("%H:%M:%S") #Taking the initital time for plot heading


#Initialize the plots
fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2, figsize=(16, 8))
ax1.set(xlabel='freq (MHz)', ylabel='power(dB)', title='Red Pitaya Channel 1 spectrum {datetime.now()}')
ax1.set_xlim(0, 62.5)
ax1.set_ylim(20, 100)
ax1.grid()

ax2.set(xlabel='freq (MHz)', ylabel='power(dB)', title='Red Pitaya Channel 2 spectrum')
ax2.set_xlim(0, 62.5)
ax2.set_ylim(20,100)
ax2.grid()

ax3.set(xlabel='Sample Time', ylabel='Total Power (dB)', title='Total Power Channel 1')
line_total_power1, = ax3.plot(time_values1, 10*np.log10(total_power1), 'b.')
ax3.grid()

ax4.set(xlabel='Sample Time', ylabel='Total Power (dB)', title='Total Power Channel 2')
line_total_power2, = ax4.plot(time_values2, 10*np.log10(total_power2), 'b.')
ax4.grid()


#Initialize the dynamic plots
ax5.set(xlabel= 'Frequency', ylabel= 'Frame', title='Dynamic Time vs. Frequency Plot- Channel 1')
im1 = ax5.imshow(power_data1, cmap=cmap, aspect='auto', origin='lower', extent=[0, n_freq_points, 0, n_time_points])
plt.colorbar(im1, ax=ax5, label='Power (dB)')


ax6.set(xlabel= 'Frequency', ylabel= 'Frame', title='Dynamic Time vs. Frequency Plot- Channel 2')
im2 = ax6.imshow(power_data2, cmap=cmap, aspect='auto', origin='lower', extent=[0, n_freq_points, 0, n_time_points])
plt.colorbar(im2, ax=ax6, label='Power (dB)')

# starting time to calculate observation time elapsed
start_time = datetime.now()

def update_plots(frame):
    current_index = frame_index[0]
    # Arm the snapshots
    fig.suptitle(f'{datetime.now()-start_time}\n',fontsize=16, y = 0.999, fontweight='bold', color = 'red')
    fpga.write_int('reg_cntrl', 1)
    fpga.snapshots.accum0_snap_ss.arm(man_trig=True)
    fpga.snapshots.accum1_snap_ss.arm(man_trig=True)

    spec0 = fpga.snapshots.accum0_snap_ss.read()['data']
    spec1 = fpga.snapshots.accum1_snap_ss.read()['data']
    fpga.write_int('reg_cntrl', 0)

    valid = np.array(spec0['val_acc0'][0:2 * acc_len * fft_len]).astype(bool)
    spectrum0 = np.array(spec0['P_acc0'][0:2 * acc_len * fft_len])
    spectrum0 = spectrum0[valid]
    spectrum0 = np.fft.fftshift(spectrum0[:256])
    
    ax1.clear()
    ax1.plot(np.linspace(-256/2, 256/2-1, 256) * 125/256, 10 * np.log10(spectrum0[:256].astype(float)), 'b-')
    ax1.set(xlabel='freq (MHz)', ylabel='power(dB)', title=f'Red Pitaya Channel 1 spectrum {datetime.now()}')    
    ax1.set_xlim(0, 62.5)
    ax1.set_ylim(20, 100)
    ax1.grid()
    
    valid = np.array(spec1['val_acc1'][0:2 * acc_len * fft_len]).astype(bool)
    spectrum1 = np.array(spec1['P_acc1'][0:2 * acc_len * fft_len])
    spectrum1 = np.fft.fftshift(spectrum1[:256])

    ax2.clear()
    ax2.plot(np.linspace(-256/2, 256/2-1, 256) * 125/256, 10 * np.log10(spectrum1[:256].astype(float)), 'b-')
    ax2.set(xlabel='freq (MHz)', ylabel='power(dB)', title=f'Red Pitaya Channel 2 spectrum {datetime.now()}')
    ax2.set_xlim(0, 62.5)
    ax2.set_ylim(20, 100)
    ax2.grid()

    
    # Update the total power plot
    total_power1.append(np.sum(spectrum0[ch1:ch2]))  # Compute total power for Ch0, adjust as needed
    time_values1.append(frame)  # Use the frame as the x-axis value
    line_total_power1.set_data(time_values1, 10 * np.log10(total_power1))
    ax3.set(xlabel='Sample Time', ylabel='Total Power (dB)', title=f'Total Power in RP channel1 - freq channel- {ch1}MHz: {ch2}Mhz - {datetime.now()}')
    ax3.relim()
    ax3.autoscale_view()
    ax3.grid()

    # Update the total power plot for channel 2
    total_power2.append(np.sum(spectrum1[ch1:ch2]))  # Compute total power for Ch0, adjust as needed
    time_values2.append(frame)  # Use the frame as the x-axis value
    line_total_power2.set_data(time_values2, 10 * np.log10(total_power2))
    ax4.set(xlabel='Sample Time', ylabel='Total Power (dB)', title=f'Total Power in RP channel2 - freq channel: {ch1}MHz - {ch2}MHz - {datetime.now()}')
    ax4.relim()
    ax4.autoscale_view()
    ax4.grid()

    ax5.clear()

    # Update the dynamic time vs. frequency plot
    current_time = datetime.now().strftime("%H:%M:%S")
    power_data1[current_index, :] = 10 * np.log10(spectrum0[128:])
    im = ax5.imshow(power_data1, cmap=cmap, aspect='auto', origin='lower', extent=[0, 62, 0, n_time_points])


    power_data2[current_index, :] = 10 * np.log10(spectrum1[128:])
    im = ax6.imshow(power_data2, cmap=cmap, aspect='auto', origin='lower', extent=[0, 62, 0, n_time_points])

    current_index = (current_index + 1) % n_time_points
    frame_index[0] = current_index

    timestamp = time.time()

    with data_lock:
        all_data.append({
            'timestamp': timestamp,
            'spec0': spectrum0,
            'spec1': spectrum1
        })

def save_data_to_csv():
    while True:
        # Check if the data should be saved and cleared (e.g., every minute)
        if len(all_data) >= 10:  # Save data every 60 entries (adjust as needed)
            with data_lock:
                current_data = all_data[:]  # Copy the data to avoid race conditions
                all_data.clear()  # Clear the data
            with open(csv_file_name, 'a', newline='') as csv_file:  # Append to the existing file
                writer = csv.DictWriter(csv_file, fieldnames=field_names)
                for data in current_data:
                    writer.writerow(data)
            print('########data dumped to the csv file#########')
        time.sleep(20)  # Adjust the sleep interval as needed (e.g., 60 seconds)


def close_event(event):
    fpga.deprogram()
    print("-----------safely escaped from ruining everything for you :) fpga deprogrammed!!-------------")
    plt.close()

csv_time = datetime.now().strftime("%H:%M")
# Define the CSV file name
csv_file_name = f'captured_data{csv_time}.csv'
# Define the CSV field names (column names)
field_names = ['timestamp', 'spec0', 'spec1']

# Create a thread for saving data to CSV
save_data_thread = threading.Thread(target=save_data_to_csv)
save_data_thread.daemon = True  # Run as a daemon thread
save_data_thread.start() # Start the thread

# Create an animation that calls the update_plots function every 500 milliseconds
ani = FuncAnimation(fig, update_plots, interval=500, cache_frame_data=False)
fig.canvas.mpl_connect('close_event', close_event)

plt.tight_layout()
plt.show()

