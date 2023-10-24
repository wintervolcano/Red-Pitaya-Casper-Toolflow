import casperfpga
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import argparse
import time
import pickle


parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help="fpg file to upload to red-pitaya")
parser.add_argument("-r", "--redpitaya", help="Red-Pitaya hostname or  IP address")
parser.add_argument("-a", "--accums", help="Number of accumulations",default=4)
parser.add_argument("-c", "--cycle", help="Number of cycles",default=5)
#parser.add_argument("--trig", default='False') 
#parser.add_argument("--man_valid", default = 'False')
#parser.add_argument("--offset", default = -1)  
#parser.add_argument("--circ_cap", default='False') 
args = parser.parse_args()


red_pitaya = args.redpitaya
print("Connecting to Red Pitaya: {0}".format(red_pitaya))
fpga=casperfpga.CasperFpga(red_pitaya)

file_fpg=args.file
print("Uploading: {0}".format(file_fpg))
fpga.upload_to_ram_and_program(file_fpg)

fft_len=256
acc_len=int(args.accums)
snap_cyc=0
print("These are the devices in your design ...")
print(fpga.listdev())

fpga.write_int('acc_len',acc_len)
fpga.write_int('snap_gap',snap_cyc)
fpga.write_int('reg_cntrl',1)

accum_cyc=int(args.cycle)
all_spec0 = {}
all_spec1 = {}
all_spec_dat = {}

#fpga.snapshots.accum0_snap_ss.arm(man_trig=args.trig, man_valid=args.man_valid, offset = int(args.offset), circular_capture = args.circ_cap)
fpga.snapshots.accum0_snap_ss.arm()
start = time.time()
# Open the files for writing before the loop
with open('spec0.npy', 'ab') as spec0_file, open('spec1.npy', 'ab') as spec1_file, open('spec_dat.npy', 'ab') as spec_dat_file:
	for i in range(accum_cyc):
		print('cycle = ', i+1)
		spec0 = fpga.snapshots.accum0_snap_ss.read()['data']

		#fpga.snapshots.accum1_snap_ss.arm()
		#spec1 = fpga.snapshots.accum1_snap_ss.read(arm=False)['data']

		#fpga.snapshots.accumdat_snap_ss.arm()
		#spec_dat = fpga.snapshots.accumdat_snap_ss.read(arm=False)['data']
		
		# Add the data to the dictionaries
		all_spec0[f'cycle_{i+1}'] = spec0
		#all_spec1[f'cycle_{i+1}'] = spec1
		#all_spec_dat[f'cycle_{i+1}'] = spec_dat

	# Save the dictionaries to .npy files
	np.save('spec0.npy', all_spec0)
	#np.save('spec1.npy', all_spec1)
	#np.save('spec_dat.npy', all_spec_dat)


# Files will be automatically closed after the with block

end = time.time()
print(start, end, 'runtime: ', (end-start), 'seconds')



	



