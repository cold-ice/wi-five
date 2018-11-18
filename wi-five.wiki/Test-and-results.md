### Setup
The antenna was placed between the flash memory and the RISC-V SoC, since it is where it makes the most sense to detect electromagnetic emissions due to the presence of the microprocessor and the external memory used to load and store data.

![HiFive1_components](/uploads/cdcb3b2080daf3a0646490975bbfc133/HiFive1_components.png)

![board](/uploads/8aefc73885816f90cd380e3139177665/board.jpg)

Due to time constraints, the acquired data covers a range from 500 KHz to 1 GHz for each test. The tests were all performed in the same room, with the laptop positioned in the same way in order to standardize as much as possible the background emissions. First of all, a general acquisition was made in order to retrieve the background emissions to subtract from the spectrum obtained when the board is turned on and executing a program. Then, the individual programs were made run and the acquisition results were saved inside separate files.

Notice that this strategy is far from being precise: the stochastic nature of many EM emissions makes so that the overall background emissions change frequently. The ideal setup consisted in making two acquisitions for each frequency range, one after another and one while the board is running and the other one while the board is off. This would allow to improve the accuracy when subtracting the two resulting power sectra. However, as explained in the previous sections, this was not possible because a proper way to automatically turn on and off the board could not be found.

In order to properly link a specific RISC-V instruction to certain EM emissions the programs loaded inside the board always consisted of a series of identical assembly instructions followed by a jump to the beginning of the program, in order to run a continuous loop. For example:

```assembly
1:  addi t0, t0, 1
    addi t0, t0, 1
    addi t0, t0, 1
    ...
    addi t0, t0, 1
    j 1b
```

### Tests
The objective of the tests I have performed was to identify bad RISC-V instructions, i.e. instructions which cause sensible electromagnetic emissions when executed in a loop and which can, in turn, be used to execute side channel attacks. The obtained data was processed in order to obtain the power spectral density in the frequency domain. Then, the obtained information were scanned with the `peak_detection` facility of the `fp` script in order to pinpoint the frequency peaks. Then, the GNU-Radio [script](addlink!) was launched in order to confirm whether the identified peaks were linked to the board. 

This test simply consisted in centering the FFT spectrum obtained in real time via GNU Radio on a range including the frequency of interest while the board was running the previously tested program. If the previously highlighted frequency emission would disappear when displacing the board away from the antenna, a correlation between the bad instruction and the EM emission could be surely established.

For reference, an example of command launched when searching for the power spectral distribution peaks is:

```bash
python fp.py -p data/addi 26 999 -e -P -d -na -w -f1 addi -f2 noise -t 120
```

The meaning of all the parameters can be easily understood by reading the [Python scripts user guide](python-scripts-user-guide) section.

The result of the tests, as well as the detected EM emissions, can be observed in the [tests](tests) folder.