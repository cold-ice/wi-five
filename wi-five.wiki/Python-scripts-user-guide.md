This page describes how to use the Python scripts developed during this project. Please refer to the [Python scripts description](python-scripts-description) to understand how the scripts work and what needs to be improved.

## td.py

Usage:

```bash
td.py [-h] [-s N] [-d] [-y p p] [-f1 filename] [-f2 filename] [-p path] [-sn filename] f f
```

This script is used to dump time domain data in complex floating point raw binary format. The default file destination is the folder "data", which should be located in the same path where the script is launched. The starting and the ending frequencies must be specified after the optional parameters. The first frequency to be specified is the starting frequency while the second one is the ending frequency. The employed antenna limits the minimum and maximum frequencies. In this implementation, as the RTL-SDR dongle is used, the frequency range is 500 kHz up to 1.75 GHz.

### Help [-h]
Prints the help for this script.

### Set sampling frequency [-s N]
Sets the sampling frequency used to acquire data in Hz. The default frequency is ca. 2.6 MHz, the maximum allowed by the RTL-SDR dongle.

### Differential acquisition [-d]
In order to use this option the script has to be run with sudo. This is thought to automatize the acquisition of data with and without the board. The objective is to be able to post process the data and isolate the frequencies emitted by the board from the background emissions. This option exploits the [Yepkit USB switchable HUB](https://www.yepkit.com/products/ykush) by Ykush. Please refer to the scripts description section for more information.

### Set Yepkit downstream hubs [-y]
This option allows to change the Yepkit downstream hubs which will be powered on or off when performing the differential acquisition. Notice that this option does nothing if `-d` is not specified.

### Set data dump filenames [-f1 filename] [-f2 filename]
With `-f1` it is possible to personalize the filename of the time domain data with the board connected while with `-f2` you may personalize the filename of the background time domain data. The default filenames are "test" and "bg". Notice that the filenames will have the relative central frequency appended at the end, before the extension (.dat). This allows the frequency processing script to correctly identify the time domain data to be processed.

### Set data dump path [-p path]
Sets the path where the time domain data will be saved for later processing with `fp.py`. Default: "./data/".

### Set data dump path [-sn filename]
Sets the name for the script launched every time the Yepkit hubs are turned on. Default: "load_program". The repository contains an example [script](https://gitlab.eurecom.fr/lanieri/wi-five/blob/master/scripts/load_program), which basically reloads the board with the program under test.

## fp.py

Usage:

```bash
fp.py [-h] [-p path] [-f1 filename] [-f2 filename] [-fs N] [-n N] [-na] [-s] [-d] [-g] [-P] [-t dB] [-e] [-fP filename] [-w] [-l] [-fw filename] [-fg filename] f f
```

This script is used to acquire data to perform post processing, such as the dB power spectrum, and to represent the result by plotting it on screen or by saving it to an output file. The processing part can be skipped if the `-l` option is specified, as preprocessed data, stored in `.npz` files, will be used instead. As previously stated, in the current version the FFT is presented in the power spectrum format and is performed by using Welch's method[^1], which consists in averaging several sets of samples to obtain a better SNR in spite of a resolution loss.

The standard output of this script is an overall frequency power spectrum plotted via [matplotlib](https://matplotlib.org/). However also a step by step plot is supported. Lastly, it is also possible to perform a spectrogram plot[^2], which allows to observe how the frequencies evolved over time. Before running this script please notice that the processing time might be long, especially if a long range of frequencies is being inspected.

### Help [-h]
Prints the help for this script.

### Set source data path [-p path]
Sets the path where the time domain data to be processed is located. Default: "./data/".

### Set data dump filenames [-f1 filename] [-f2 filename]
With `-f1` it is possible to set the filename of the time domain data with the board connected while with `-f2` you may personalize the filename of the background time domain data. These are the filenames of the floating point, complex raw binary data which will be processed. The default filenames are "test" and "bg". The `-f2` optional parameter is useful only if you want to perform differential data processing. Notice that the filenames **must** have the relative central frequency appended at the end for the script to correctly identify and process them in the proper order. Also, the files extension **must** be .dat.

### Set sampling frequency [-s N]
Sets the sampling frequency of the processed data in Hz. The default frequency is ca. 2.6 MHz, the maximum allowed by the RTL-SDR dongle.

### Set FFT size [-n N]
Sets the FFT size of each FFT transform. The higher the number of points the more accurate the FFT. Defaults to 16383, which is the maximum allowed by GNU radio. An even higher number can be used, however consider it will negatively impact the processing speed.

### Disables overall power spectrum plot [-na]
Use this option if you want to disable the plot of the overall power spectrum which has been produced. Notice that if `-S` is not specified no screen output will be produced.

### Enable step by step power spectrum plotting [-s]
This option enables the step by step output of frequency power spectra. In a nutshell, the various produced power spectra will be printed one by one on screen. Notice that this option doesn't disable the overall spectrum plot.

### Perform differential analysis [-d]
Add this parameter if you have acquired data with and without the board and you wish to remove the background frequencies to isolate only the ones emitted by the board. If this option is selected three plots will be output to screen: the power spectrum of the board data, the power spectrum of the background data and the power spectrum of the distance between the two. The script will look inside the path (default: "./data/") for the raw binary files of the acquisitions with the board (default name: "test[f].dat", where f represents the central frequency), then it will look for the acquisitions of the background noise (default name: "bg[f].dat", where f represents the central frequency), then it will subtract the latter spectrum from the former one to _try_ to isolate the board frequencies. Notice that this process is hugely perfectible and it was the main challenge of this project.

### Show spectrogram [-g]
This option enables the spectrogram plot of the processed data. Notice that if the `-d` option is selected three spectrograms will be produced for each inspected range, following the same strategy adopted for the frequency spectra. Moreover, the spectrograms will be stored inside `.npz` files if the `-w` option is selected.

### Find peaks [-P]
Enables the search of peaks in the output power spectra.

### Set peak threshold [-t dB]
Sets the minimum power in dB which a peak should have. This option is useless if `-P` has not been specified. The default value is -50. 

### Export peaks [-e]
Enables the export of the detected peaks. The output will be printed in a file, with the peak frequency on the left column and the peak magnitude in dB on the right column. This option is useless if `-P` has not been specified. The output file will be saved in the destination path (default: "./data/").

### Set filename for peaks export [-fP]
Sets the filename of the export file containing the detected peaks. This option is useless if `-P` and `-e` have not been specified. The default name is "scan_". The current data and time will be appended to the filename, to avoid rewriting previous peak exports. The extension of the file is .txt.

### Export compressed data [-w]
With this option all the produced data will be exported to .npz files inside the working path. This includes all the power spectra and spectrograms produced. The .npz files can be later reused to perform peak analysis or to plot them, allowing to skip the processing part.

### Load compressed data [-l]
Data will be loaded from .npz files instead of being processed from raw binary files. Obviously, this will speed up the script execution. The files will be searched for in the working path (it's worth to remember that it can be changed with the `-p` option). Please notice that the specified options influence the necessary .npz files. For instance, if the `-g` option is specified, the spectrogram .npz archive must be available. Notice also that the input .npz archives must have precise suffixes, based on their destination. Following is the complete list:  
  * Overall power spectrum: <fft_filename>.npz
  * If the `-d` option is specified:
    * Power spectrum with device: <fft_filename>_P1.npz
    * Power spectrum without device: <fft_filename>_P2.npz
  * If the `-g` option is specified:
    * Overall spectrogram: <spg_filename>.npz
    * If the `-d` option is specified:
      * Spectrogram with device: <spg_filename>_S1.npz
      * Spectrogram with device: <spg_filename>_S2.npz
When data is loaded from .npz archives the step by step plotting is not supported, i.e. the `-s` option has no effect. Please refer to the following sections to understand how to specify filenames which differ from the default ones (fft_filename defaults to `fft_export` and spg_filename defaults to `spg_export`).

### Set filename for frequency spectrum export [-fw]
With this option you may specify the filename for the frequency spectrum .npz archive. This filename is used both when storing data and when loading data in order to produce plots or to export peaks. The .npz archives filename defaults to `fft_export`. Notice that the .npz extension is automatically appended to the file.

### Set filename for spectrogram export [-fg]
With this option you may specify the filename for the spectrogram .npz archive. This filename is used both when storing data and when loading data in order to produce spectrograms. The .npz archives filename defaults to `spg_export`. Notice that the .npz extension is automatically appended to the file.

[^1]: Welch, P. D. (1967), "The use of Fast Fourier Transform for the estimation of power spectra: A method based on time averaging over short, modified periodograms", IEEE Transactions on Audio and Electroacoustics, AU-15 (2): 70–73, doi:[10.1109/TAU.1967.1161901](https://doi.org/10.1109%2FTAU.1967.1161901)

[^2]: Oppenheim, Alan V., Ronald W. Schafer, John R. Buck “Discrete-Time Signal Processing”, Prentice Hall, 199