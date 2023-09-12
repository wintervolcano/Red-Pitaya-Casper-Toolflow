# Vivado-Installation

While installing Vivado by xilinx, the installer was getting stuck at the generating devices list... stage.

To bypass this, we can do:

doUbuntu()
{
### AIE Tools prerequisite libraries
   apt-get update | tee -a $logFile 
   apt-get install -y libc6-dev-i386 net-tools | tee -a $logFile 
   apt-get install -y graphviz | tee -a $logFile 
   apt-get install -y make | tee -a $logFile 
### Vitis Tools prerequisite libraries
   apt-get install -y unzip | tee -a $logFile
   apt-get install -y g++ | tee -a $logFile
   apt-get install -y libtinfo5 | tee -a $logFile
   apt-get install -y xvfb | tee -a $logFile
   apt-get install -y git | tee -a $logFile
   apt-get install -y libncursesw5 | tee -a $logFile
   apt-get install -y libc6-dev-i386 | tee -a $logFile
}

Then Install the software normally



## progska error fix:

sudo apt-get --reinstall install libc6 libc6-dev

Fixed it!


## build issues 

https://bobbyhadz.com/blog/python-error-invalid-command-bdist-wheel


This issue is caused by  library dependency differences between what Ubuntu 
base uses and what the Xilinx Model Composer and MATLAB Simulink are wanting to 
use. Particularly the various libgmp libraries used.

To side step this issue requires altering your Model Composer installation 
directory. I have been successful in making these adjustments. But, altering 
the installation may have other consequences and not generally recommended. 
That being said I have not as of yet had any compatibility or seen any failures 
result because of it.

Assuming you have Xilinx installations at `/opt/Xilinx` (or change this path 
for where your installation is)

```
cd /opt/Xilinx/Model_Composer/2021.1/lib/lnx64.o/Ubuntu
mkdir exclude
mv libgmp.so* exclude/

cd /opt/Xilinx/Vivado/2021.1/lib/lnx64.o/Ubuntu
mkdir exclude
mv libgmp.so* exclude/

cd /opt/Xilinx/Vivado/2021.1/lib/lnx64.o
mkdir exclude
mv libgmp.so* exclude/
```
The libgmp that match the wild card will be moved to the exclude directory and 
not searchable when Model Composer and Simulink are load up. If you have any 
issues the process is reversed by placing the files in the `exclude/` directory 
back into their previous locations.




In case others are struggling with this problem...


When running a simulation in my Ubuntu 20.04 system I got "Error: no such 
## instruction: `endbr64'".

I spent a lot of time on this including making links to /usr/include without 
success. Then I tried

        !gcc /tmp/hello.c

/tmp/cc2Od0Ug.s: Assembler messages:
/tmp/cc2Od0Ug.s:12: Error: no such instruction: `endbr64'

        !which as

/srv/data/opt/Xilinx/Vivado/2021.1/tps/lnx64/binutils-2.26/bin/as

in the Matlab console. Aha! The problem is obvious because the version of the 
system as is 2.34.

```
cd  /tools/Xilinx/Vivado/2021.1/tps/lnx64/binutils-2.26 I
mv bin bin.bak
```
and compiling and simulating now works!


## To update the license for Xilinx

/tools/Xilinx/Vivado/2021.1/bin/vlm
