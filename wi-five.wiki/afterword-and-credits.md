### Lessons learned
This project taught be a lot about Python and the data processing facilities offered by functions such as Numpy and Scipy. Reading several articles on signal processing and EM emissions surely expanded my knowledge on these technical aspects. Moreover, I touched with hands how hard it is to properly isolate EM emissions coming from an embedded systems when the surrounding environment is particularly noisy, in particular due to the fact that these emissions are generally very low power. Clearly these issues will not be encountered if a way to strengthen the EM emissions coming from the HiFive1 board is employed, or if the tests are performed inside an anechoic chamber.

Nonetheless, in my opinion, realizing an environment which could allow to make statements on the EM emissions coming from a HiFive1 Board, and, in general, coming from any embedded systems, could be extremely useful. It would allow to identify right away the critical information coming from the EM side-channel even when proper testing equipment is not available, such as during early testing phases. My work, I believe, has demonstrated that this is achievable, even though the final results may not be perfect and as precise as when testing in a proper environment and while using the proper equipment.

Many papers have thoroughly demonstrated to which extent can EM emissions be exploited to attack embedded systems. Having another ace up the developers' sleeve to counteract this issue should be worth the time spent on it.

### Credits
I wish to thank professor [Aurelien Francillon](http://s3.eurecom.fr/~aurel/) for giving me the chance to work on this project and for supporting me with very useful intel and also by providing me with all the employed hardware.

A big thank you goes as well to [Giovanni Camurati](http://www.eurecom.fr/en/people/camurati-giovanni/biography), currently a PhD student at Eurecom, who gave me very precious tips when testing and developing the scripts, other than giving other very useful general advices.

The [detect_peaks.py](https://gitlab.eurecom.fr/lanieri/wi-five/blob/master/scripts/detect_peaks.py) Python code was developed by [Marcos Duarte](https://github.com/demotu/BMC), who deserves all the credit for it. It was used since the general Python libraries don't contain a peak detection script as efficient and as customizable as this one.

### Contact information
In case of doubts or questions on this project send me an email at:  
[lanieri@eurecom.fr](mailto:lanieri@eurecom.fr)