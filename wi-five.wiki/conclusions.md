The realized scripts represent, in my opinion, a good start in terms of realizing an environment which allows to analyze EM emissions coming from an embedded system across multiple ranges, be it the HiFive1 board or anything else. In particular, its points of strength are the capability of digesting a large amount of data, the possibility to quickly resume the previously produced spectral information by importing preprocessed data from .npz archives and the fact that all these scripts can be easily adapted for any type of antenna which can be operated via an OS.

However, in spite of all my efforts, not many critical frequencies could be exposed. The reasons are manifold:
* the proper script testing was started too late;
* the `peak_detection` function needs to be properly tuned, as too many peaks are pinpointed, making the verification excessively long;
* the adopted method to filter out the frequencies is **too rudimentary**: there surely exists a better way to find the differences between two spectra than simply computing a difference;

Should a future version of the `fp.py` script be developed, the aforementioned issues should be addressed. Testing how the various parameters of the `detect_peaks` function influence the results (e.g.: change the `mpd` and/or the `mph` parameters and see if the results improve) is a good starting point. Possibly there might even be a way to automatically set these input parameters given the input data in order to give an optimal/semi optimal result. Or an ad hoc peak detection function could be developed.

Moreover, as previously stated:
* the iteration step in both `td.py` and `fp.py` should be made dependent on the sampling frequency, in order to produce the proper amount of frequency spectra, as right now these functions work properly only if the sampling frequency amounts to 2 MHz;
* the `f1` and `f2` input parameters must not be asked if the `-l` input is specified, as the data concerning f<sub>0,min</sub> and f<sub>0,max</sub> comes directly from the .npz archive;
* lastly, it might be a good idea to rewrite the `td` script in such a way that also other antennas can be used, not just the RTL-SDR dongle;

In this section I wanted to pinpoint the most critical issues. Others might be present, of course. Should someone start working on these scripts the [afterwords](afterwords-and-credits) section contains my contact information in case of need of additional information or in case of doubts.