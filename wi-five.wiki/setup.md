## Install dependencies and download GitLab repository
The following steps will guide you through the installation of the necessary dependencies to run the Python scripts contained in this repository.

1. Update apt-get repositories

    ```bash
    $ sudo apt-get update
    ```
2. Install `gnuradio`

    ```bash
    $ sudo apt-get install gnuradio
    ```
1. The next steps involve downloading several repositories from GitHub, hence you might want to enter an installation directory before proceeding, e.g.:

    ```bash
    $ mkdir ~/wifive-dependencies && cd ~/wifive-dependencies
    ```
1. Install `RTL-SDR` drivers ([reference](https://www.rtl-sdr.com/rtl-sdr-quick-start-guide/))

    Auto:
    ```bash
    $ sudo apt-get install rtl-sdr
    ```
    Manual:
    ```bash
    $ sudo apt-get install libusb-1.0-0-dev git cmake
    $ git clone git://git.osmocom.org/rtl-sdr.git
    $ cd rtl-sdr/
    $ mkdir build
    $ cd build
    $ cmake ../ -DINSTALL_UDEV_RULES=ON
    $ make
    $ sudo make install
    $ sudo cp ../rtl-sdr.rules /etc/udev/rules.d/
    $ sudo ldconfig
    ```
1. Unload the `DVB-T drivers`, used by default by Linux, in order to be able to use the proper RTL-SDR antenna drivers

    ```bash
    $ echo 'blacklist dvb_usb_rtl28xxu' | sudo tee --append /etc/modprobe.d/blacklist-dvb_usb_rtl28xxu.conf
    ```
    Notice that this is a permanent solution. If you want to unload these drivers only temporarily run instead:  

    ```bash
    $ sudo rmmod dvb_usb_rtl28xxu
    ```
1. Install the RTL-SDR Gnuradio blocks ([reference](https://osmocom.org/projects/rtl-sdr/wiki/Rtl-sdr))

    ```bash
    $ git clone git://git.osmocom.org/gr-osmosdr
    $ cd gr-osmosdr/
    $ mkdir build
    $ cd build/
    $ cmake ../
    $ make
    $ sudo make install
    $ sudo ldconfig
    ```
1. Install `USB` Python library

    ```bash
    $ sudo pip install pyusb
    ```

1. Install `correctiq` Gnuradio block

    ```bash
    $ git clone https://github.com/ghostop14/gr-correctiq.git
    $ cd gr-correctiq
    $ mkdir build
    $ cd build
    $ cmake ..
    $ make
    $ make install
    $ ldconfig
    ```

1. Install drivers for the `ykush board`. Notice that internet connection is required to run the .sh scripts ([reference](https://www.yepkit.com/learn/setup-guide-ykush))

    ```bash
    $ sudo apt-get install libusb-1.0-0-dev 
    $ sudo apt-get install libusb-1.0-0
    $ git clone https://github.com/Yepkit/ykush.git
    $ cd ykush
    $ sudo ./build.sh
    $ sudo ./install.sh
    ```
1. You are now able to run the scripts contained in this repository, which are located in the scripts subdirectory. There is no need to install them, all you have to do is run:

    ```bash
    $ git clone https://gitlab.eurecom.fr/lanieri/wi-five.git
    ```
1. Lastly, you might want to create a directory where you will store all the raw data files. To create the default one:

    ```bash
     $ mkdir wi-five/scripts/data
     ```

## Setup the Freedom SDK for the board

Following are the instructions to setup the software development kit for the [HiFive1](https://www.sifive.com/products/hifive1/) board ([reference](https://static.dev.sifive.com/dev-kits/hifive1/hifive1-getting-started-v1.0.2.pdf)).

1. After having connected the HiFive1 board via USB check that it has been recognized by Linux

    ```bash
    $ lsusb
    ```
    Among the connected devices you should find:  
    Bus XXX Device XXX: ID 0403:6010 Future Technology Devices
    International, Ltd FT2232C Dual USB-UART/FIFO IC
1. Set the `udev` rules to allow the `plugdev` group to access the device

    ```bash
    $ sudo vi /etc/udev/rules.d/99-openocd.rules
    ```
    Add the following lines and save the file (if they are not already there):  
    
    ```
    # These are for the HiFive1 Board
    SUBSYSTEM=="usb", ATTR{idVendor}=="0403",
      ATTR{idProduct}=="6010", MODE="664", GROUP="plugdev"
    SUBSYSTEM=="tty", ATTRS{idVendor}=="0403",
      ATTRS{idProduct}=="6010", MODE="664", GROUP="plugdev"
    # These are for the Olimex Debugger for use with E310 Arty Dev Kit
    SUBSYSTEM=="usb", ATTR{idVendor}=="15ba",
      ATTR{idProduct}=="002a", MODE="664", GROUP="plugdev"
    SUBSYSTEM=="tty", ATTRS{idVendor}=="15ba",
      ATTRS{idProduct}=="002a", MODE="664", GROUP="plugdev"
    ```
1.  Check that the board shows up as a serial device belonging to the `plugdev` group

    ```bash
    $ ls /dev/ttyUSB*
    ```
    If you have other serial devices or multiple boards attached you may have more devices listed. For serial communication with the UART always select the device with the higher number, e.g. if the responses are /dev/ttyUSB0 and /dev/ttyUSB1, you should check the latter:

    ```bash
    $ ls -l /dev/ttyUSB1
    ```
The answer should be:

    ```bash
    crw-rw-r-- 1 root plugdev 188, 1 Nov 28 12:53 /dev/ttyUSB1
    ```
1. Add yourself to the `plugdev` group.

    ```bash
    $ sudo usermod -a -G plugdev <yourusername>
    ```
1. Log out and log back in, then check that you're part of the `plugdev` group
    
    ```bash
    $ groups
    ```
1. Connect to the board with a terminal emulator, e.g. `screen`, to make sure that you may access the serial (UART) and debug interface without sudo permissions

    ```bash
    $ sudo screen /dev/ttyUSB1 115200
    ```
    Regardless of the terminal emulator, the baudrate must be set to 115200, the parity bit option must not be active and the number of data and stop bits must be set respectively to 8 and 1. If you managed to connect to the board via UART the SiFive logo should appear on the terminal, followed by "'led_fade' Demo" and by a user input request.

1. It is now possible to install the Freedom E Software Development Kit. Clone the relative GitHub repository and enter the main folder

    ```bash
    $ git clone --recursive https://github.com/sifive/freedom-e-sdk.git
    $ cd freedom-e-sdk
    ```
1. Read the README.md file and install all the necessary packages.

1. You may now build the software toolchain, optionally specifying the HiFive1 board as the default one. Please mind that the installation process is rather lengthy and you might want to add the `-j N` option to speed up the process, with N being the number of cores you wish to use, if you are working with a multi-core processor

    ```bash
    $ make tools BOARD = freedom-e300-hifive1
    ```
    or simply

    ```bash
    $ make tools BOARD = freedom-e300-hifive1
    ```
1. The Freedom E SDK toolchain is now installed. It might be a good idea to check for repository updates now and then. Needless to say, however, software updates may bring compatibility issues, so you might want to **think twice before updating the SDK**. In case you wish to do so run: 

    ```bash
    $ git pull origin master
    $ git submodule update --init --recursive
    ``` 
    If any updates are found simply rerun the command described in the previous point to update the SDK. 

## Build, run and debug programs on the HiFive1 board
1. The source code must be placed inside a subfolder within the "software" directory. Inside, you may find some default examples. They include Makefiles which can be used as a reference when developing your own code. In order to compile a program, make sure you are in the main repository folder ("freedom-e-sdk", by default) and run:

    ```bash
    $ make software [PROGRAM=<program-directory-name> BOARD=<board-name>]
    ```
The value of the PROGRAM variable must be the name of the folder containing the target software. The BOARD variable is _always_ optional and defaults to the one provided when installing the SDK or to "freedom-e300-hifive1", if none has been provided. The PROGRAM variable is also always optional and defaults to "demo_gpio".

1. It is now possible to upload the compiled software to the HiFive1 board by running:

    ```bash
    $ make upload [PROGRAM=<program-directory-name> BOARD=<board-name>]
    ```

1. If you wish to run GDB:
    1. Open an OpenOCD connection to the board in a separate terminal window:

        ```bash
        $ make run_openocd [BOARD=<board-name>]
        ```
    1. Run the following command to run the chosen program with GDB on the board. Notice that the connection between the terminal and the board has obviously been opened by OpenOCD: 
    
        ```bash
        $ make run_gdb [PROGRAM=$(PROGRAM) BOARD=$(BOARD)]
        ```
1. To visualize all the Makefile options simply run:

    ```bash
    $ make
    ```