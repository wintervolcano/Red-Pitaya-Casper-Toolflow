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
