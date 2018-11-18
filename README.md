# Wi-five
Repository for a semester project at Eurecom, promo 2019.

Professor: Aurelien Francillon  
PhD Assistant: Giovanni Camurati  
Student: Valerio Lanieri  

[Wiki](wi-five.wiki/home.md)

### Log 22/06/2018
I have added several functionalities to the script:
  * possibility to export produced data;
  * possibility to import produced data;
  * possibility to show spectrogram;
  
I will work on the report, trying to finish all the technical parts by the weekend.

### Log 17/06/2018
Written some more of the report, added the possibility to pass options to the scripts through the commandline.

### Log 08/06/2018
I have started to write the report of the project and did some acquisition tests with the Python scripts, compiling several assembly programs and uploading them to the HiFive1 board. There are still many issues regarding the isolation of useful frequencies.

### Log 02/06/2018
I have added the possibility to turn on and off the FPGA board/HiFive1 board via the Yepkit USB switchable hub. Unfortunately, I can't program the FPGA board/the HiFive1 board when the Yepkit hub is "in the way" (it probably just provides power, no control signals connection).

### Log 25/05/2018
I have tested the script with Giovanni and also retrieved an Olimex Jtag connector and some other materials to be able to program the FPGA board.

### Log 18/05/2018
I found a useful Python script (detect_peaks.py) and implemented it inside the processing script to detect the peaks of the obtained power spectra. I still haven't had the chance to work on the acquisiton of frequencies when running a certain program on the FPGA.

### Log 13/05/2018
I was able to setup the FPGA board and I made some tests with the function that computes the difference between two spectrums. I tried several approaches and kept the most suited one.

### Log 02/05/2018
Fixed issue: gnuradio was removed by a package installed fro CompMeth project. I take advantage of the mishap to review how to install gnuradio and the rtl-sdr blocks, this will be written on the final report.  
Links:  
Installing rtlsdr: [https://www.rtl-sdr.com/rtl-sdr-quick-start-guide/](https://www.rtl-sdr.com/rtl-sdr-quick-start-guide/)  
(to install gnuradio sudo apt-get install gnuradio)  
Installing rtlsdr blocks: [http://osmocom.org/projects/sdr/wiki/rtl-sdr](http://osmocom.org/projects/sdr/wiki/rtl-sdr)  
Unfortunately, a **short circuit** seem to have ensued and the board doesn't seem to work properly any longer (it emits an audible buzzing sound and it warms up noticeably and quickly). I will have to setup the FPGA board to continue the tests. On the bright side, I made many progresses concerning the Python script which should automatically read several frequencies, make a difference between two FFTs and reveal the frequencies of interest.

### Log 22/04/2018
I could not do much this week due to the Formal Methods exam on the 26th. I read some of the proposed articles and noted useful references.

### Log 14/04/2018
This log sums up all the work done up until now:
* The file [led\_test](data/led_test.md) contains a table with all the frequencies which could be linked to the board when running the `led\_blink' sample program. This is kind of useless as I can't relate these emissions to any specific instruction, however it is useful to run tests
* The `scripts` folder contains .c files and .grc and .m scripts used to perform digital signal processing duties. The .grc scripts are used to generate .py scripts which in turn either acquire data from the antenna, perform dsp or sink the data to binary files. The raw2num*.c scripts are used to turn binaries into either integer, floating point or complex floating point vectors. The matlab script [wifive\_dsp](scripts/wifive_dsp.m) is used to manually perform fft.
* The first "milestone" of this project is to be to be capable of scanning multiple frequency ranges and telling board emissions from the environment. The main goal is to relate the detected emissions to specific RISC V assembly instructions. The work done up until now allowed me to better understand GNURadio and to review how the fft is performed.
