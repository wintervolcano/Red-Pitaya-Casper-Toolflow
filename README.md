# Vivado-Installation

https://community.element14.com/technologies/fpga-group/b/blog/posts/installing-xilinx-vivado-on-ubuntu

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




## Cannot write to register

https://www.mail-archive.com/casper@lists.berkeley.edu/msg02503.html



####     Error evaluating 'OpenFcn' callback of Xilinx Adder/Subtracter Block block (mask) 'IIR_DirectForm_3pole_1/AddSub'. Callback string is 'xlOpenGui(gcbh, 'addsub_gui.xml', @addsubenablement, -1)' 
#### Error using xlNMIProxy Timed out waiting for a response from GUI to: (2.0001) buildGUI DISPLAY ENV = ":0" timeout value = 180.0014


This is a Qt4 package issue. 

Double-clicking should open a block in a loaded SLX model.  No window opens, and after very long pause, a dialog appears with an error message, it reads
Error evaluating 'OpenFcn' callback of Xilinx Type Reinterpreter Block block (mask) 'zcu216_tut_spec_cx/Reinterpret9'. Callback string is 'xlOpenGui(gcbh, 'reinterpret_gui.xml',@reinterpretenablement,-1)' .  Error using xlNMIProxy Timed out waiting for a response from GUI to: (74880.0001) buildGUI DISPLAY ENV =":0" timeout value = 180.0013

This error is caused by sysgensockgui failing to load.  The non-loading is likely caused by missing dependencies.  One these are resolved, sysgensockgui should operate as intended. Missing dependencies can be checked the following way,
````
root@r*****a:/tools/Xilinx/Vivado/2021.1/bin# ldd unwrapped/lnx64.o/sysgensockgui 
        linux-vdso.so.1 (0x00007ffedf51e000)
        libQtCore.so.4 => not found
        libQtGui.so.4 => not found
        libQtNetwork.so.4 => not found
        libQtXml.so.4 => not found
        librdi_itlib.so => not found
        libstdc++.so.6 => /lib/x86_64-linux-gnu/libstdc++.so.6 (0x00007fddc2160000)
        libm.so.6 => /lib/x86_64-linux-gnu/libm.so.6 (0x00007fddc200f000)
        libgcc_s.so.1 => /lib/x86_64-linux-gnu/libgcc_s.so.1 (0x00007fddc1ff4000)
        libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007fddc1e02000)
        /lib64/ld-linux-x86-64.so.2 (0x00007fddc2367000)


````

"sysgensockgui" needs the entire framework of Qt 4.8.x to run correctly. If you have Qt 4 install in your system, those should be taken care for you.

The four libraries libQtCore.so.4, libQtGui.so.4, libQtNetwork.so.4, and libQtXml.so.4 is our version of the Qt 4 libraries. It will be overloaded when you launch the SysGen blocks within the Qt 4 framework.

### Solution
```
sudo add-apt-repository ppa:rock-core/qt4
sudo apt-get update
sudo apt-get install libqtcore4
sudo apt-get install libqtgui4
```
