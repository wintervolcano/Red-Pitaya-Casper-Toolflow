import numpy as np
import matplotlib.pyplot as plt
import sys

# Arguments passed
print("\nName of datafile:", sys.argv[1])

datafile = sys.argv[1]
cycle = sys.argv[2]
#spec0 = np.load(datafile, allow_pickle=True)
spec0 = np.load('spec0.npy', allow_pickle=True)
P_acc0 = spec0.item().get(cycle).get('P_acc0')

fig,ax = plt.subplots(4,4)
for idx in range(16):
	x1 = idx *256
	x2 = 256 * (idx + 1)
	#print(x1,x2)
	ax[int(idx/4),np.mod(idx,4)].plot(P_acc0[x1:x2])
	ax[int(idx/4),np.mod(idx,4)].set_ylim(0,1.3e7)
	print(int(idx/4),np.mod(idx,4))
	
print('Number of cycles in file :',spec0.item().keys())
print(len(P_acc0))
print('Total data length = ', len(P_acc0) * len(spec0.item().keys()))
#plt.plot(P_acc0)
plt.show()
