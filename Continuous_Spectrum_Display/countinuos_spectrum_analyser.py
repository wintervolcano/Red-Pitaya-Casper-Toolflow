import casperfpga
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import argparse
import time

parser = argparse.ArgumentParser()
parser.add_argument("-a", "--accums", help="Number of accumulations",default=5)
args = parser.parse_args()

fpga=casperfpga.CasperFpga('rp-f05ad8.local')
fpga.upload_to_ram_and_program('tut_spec.fpg')


fft_len=256
acc_len=int(args.accums)
snap_cyc=10
# print("These are the devices in your design ...")
# print(fpga.listdev())

fpga.write_int('acc_len',acc_len)
fpga.write_int('snap_gap',snap_cyc)

#Initialize the figures and axes
# fig0, ax0 = plt.subplots()
# ax0.set(xlabel='channel', ylabel='power', title='Ch0')
# ax0.set_xlim(0, 2 * acc_len * fft_len)

# fig1, ax1 = plt.subplots()
# ax1.set(xlabel='channel', ylabel='power', title='Ch1')
# ax1.set_xlim(0, 2 * acc_len * fft_len)

fig2, ax2 = plt.subplots()
ax2.set(xlabel='freq (MHz)', ylabel='power(dB)', title='Ch0')
ax2.set_xlim(0, 50)

# fig3, ax3 = plt.subplots()
# ax3.set(xlabel='freq (MHz)', ylabel='power', title='Ch1')
# ax3.set_xlim(0, 50)


def update_plots(frame):
	# Arm the snapshots
	fpga.write_int('reg_cntrl',1)
	fpga.snapshots.accum0_snap_ss.arm(man_trig=True)
	# fpga.snapshots.accum1_snap_ss.arm(man_trig=True)
	# fpga.snapshots.accumdat_snap_ss.arm(man_trig=True)
	# time.sleep(5)
	spec0=fpga.snapshots.accum0_snap_ss.read()['data']
	# spec1=fpga.snapshots.accum1_snap_ss.read()['data']
	fpga.write_int('reg_cntrl',0)

	# Update the plots
	# ax0.clear()
	# ax0.plot(np.array(spec0['val_acc0'][0:2 * acc_len * fft_len]).astype(float) * 5e7, 'r-.')
	# ax0.plot(spec0['P_acc0'][0:2 * acc_len * fft_len], 'b-')
	# ax0.set(xlabel='channel', ylabel='power', title='Ch0')
	# ax0.set_xlim(0, 2 * acc_len * fft_len)

	# ax1.clear()
	# ax1.plot(np.array(spec1['val_acc1'][0:2 * acc_len * fft_len]).astype(float) * 5e7, 'r-.')
	# ax1.plot(spec1['P_acc1'][0:2 * acc_len * fft_len], 'b-')
	# ax1.set(xlabel='channel', ylabel='power', title='Ch1')
	# ax1.set_xlim(0, 2 * acc_len * fft_len)

	valid = np.array(spec0['val_acc0'][0:2 * acc_len * fft_len]).astype(bool)
	spectrum0 = np.array(spec0['P_acc0'][0:2 * acc_len * fft_len])
	spectrum0 = spectrum0[valid]
	spectrum0 = np.fft.fftshift(spectrum0[:256])
	ax2.clear()
	ax2.plot(np.linspace(-256/2, 256/2-1, 256) * 125/256, 10*np.log10(spectrum0[:256].astype(float)), 'b-')
	ax2.set(xlabel='freq (MHz)', ylabel='power', title='Ch0')
	ax2.set_xlim(0, 50)
	ax2.set_ylim(20,100)
	ax2.grid()
	
	# valid = np.array(spec1['val_acc1'][0:2 * acc_len * fft_len]).astype(bool)
	# spectrum1 = np.array(spec1['P_acc1'][0:2 * acc_len * fft_len])
	# spectrum1 = np.fft.fftshift(spectrum1[:256])

	# ax3.clear()
	# ax3.plot(np.linspace(-256/2, 256/2-1, 256) * 125/256, spectrum1[:256].astype(float), 'b-')
	# ax3.set(xlabel='freq (MHz)', ylabel='power', title='Ch1')
	# ax3.set_xlim(0, 50)

# Create an animation that calls the update_plots function every second
ani = FuncAnimation(plt.gcf(), update_plots, interval=500)

plt.show()