all_spec0 = {}
all_spec1 = {}
all_spec_dat = {}

for i in range(accum_cyc):
    print('cycle = ', i+1)
    fpga.snapshots.accum0_snap_ss.arm()
    spec0 = fpga.snapshots.accum0_snap_ss.read(arm=False)['data']

    fpga.snapshots.accum1_snap_ss.arm()
    spec1 = fpga.snapshots.accum1_snap_ss.read(arm=False)['data']

    fpga.snapshots.accumdat_snap_ss.arm()
    spec_dat = fpga.snapshots.accumdat_snap_ss.read(arm=False)['data']

    # Add the data to the dictionaries
    all_spec0[f'cycle_{i+1}'] = spec0
    all_spec1[f'cycle_{i+1}'] = spec1
    all_spec_dat[f'cycle_{i+1}'] = spec_dat

# Save the dictionaries to .npy files
np.save('spec0.npy', all_spec0)
np.save('spec1.npy', all_spec1)
np.save('spec_dat.npy', all_spec_dat)








# Open the files for writing before the loop
with open('spec0.npy', 'ab') as spec0_file, open('spec1.npy', 'ab') as spec1_file, open('spec_dat.npy', 'ab') as spec_dat_file:
    for i in range(accum_cyc):
        print('cycle = ', i+1)
        fpga.snapshots.accum0_snap_ss.arm()
        spec0 = fpga.snapshots.accum0_snap_ss.read(arm=False)['data']

        fpga.snapshots.accum1_snap_ss.arm()
        spec1 = fpga.snapshots.accum1_snap_ss.read(arm=False)['data']

        fpga.snapshots.accumdat_snap_ss.arm()
        spec_dat = fpga.snapshots.accumdat_snap_ss.read(arm=False)['data']

        # Append spec0 to the binary file
        np.save(spec0_file, spec0)

        # Append spec1 to the binary file
        np.save(spec1_file, spec1)

        # Append spec_dat to the binary file
        np.save(spec_dat_file, spec_dat)

# Files will be automatically closed after the with block

