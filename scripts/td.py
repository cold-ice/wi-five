#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""Time domain data dump script"""

##################################################
# GNU Radio Python Flow Graph
# Title: Data Sink2
# Generated: Mon Apr 23 17:34:41 2018
##################################################

#Credits: https://gist.github.com/PaulFurtado/fce98aef890469f34d51

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import osmosdr # must be installed
import time
import correctiq # to perform 0 DC IQ correction, must be installed
import subprocess

#from usb.core import find as finddev # to install this library: sudo pip install pyusb
  
import argparse

parser = argparse.ArgumentParser(description='Stores frequency data in time domain from a specified frequency range')
parser.add_argument('frequency', metavar='f', type=int, nargs=2, default=[26, 28], help='frequency range')
parser.add_argument('-s', '--Fs', metavar='N', type=float, default=2e6, help='set sampling frequency of input data')
parser.add_argument('-d', '--diff', action='store_true', help='stores data with and without board activity - needs to be run with SUDO!')
parser.add_argument('-y', metavar='p', nargs=2, default=['1', '2'], help='select ykush board ports')
parser.add_argument('-f1', '--filename1', metavar='filename', default="test", help='set filename for test dump')
parser.add_argument('-f2', '--filename2', metavar='filename', default="bg", help='set filename for background dump')
parser.add_argument('-p', '--path', metavar='path', default="./data", help='set path for data dumps')
parser.add_argument('-sn', '--script', metavar='filename', default="load_program", help='set name for script to be run during differential acquisition')

args = parser.parse_args()

fmin = args.frequency[0]
fmax = args.frequency[1]
Fs = args.Fs
if fmax<fmin:
    print("Error: fmin larger than fmax")
    quit()
ykush_on = args.diff
ykush1 = args.y[0]
ykush2 = args.y[1]
test_name = args.filename1
noise_name = args.filename2
scriptname = args.script

class data_sink2(gr.top_block):

    path = args.path+"/"
    print path

    def __init__(self):
        gr.top_block.__init__(self, "Data Sink2")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = Fs
        self.f0 = f0 = fmin
        self.path = path = data_sink2.path
        self.filename = filename = test_name+str(fmin)+".dat"

        ##################################################
        # Blocks
        ##################################################
        self.rtlsdr_antenna = osmosdr.source( args="numchan=" + str(1) + " " + "" )
        self.rtlsdr_antenna.set_sample_rate(samp_rate)
        self.rtlsdr_antenna.set_center_freq(f0, 0)
        self.rtlsdr_antenna.set_freq_corr(0, 0)
        self.rtlsdr_antenna.set_dc_offset_mode(0, 0)
        self.rtlsdr_antenna.set_iq_balance_mode(0, 0)
        self.rtlsdr_antenna.set_gain_mode(False, 0)
        self.rtlsdr_antenna.set_gain(40, 0)
        self.rtlsdr_antenna.set_if_gain(20, 0)
        self.rtlsdr_antenna.set_bb_gain(20, 0)
        self.rtlsdr_antenna.set_antenna("", 0)
        self.rtlsdr_antenna.set_bandwidth(0, 0)

        self.data_sink = blocks.file_sink(gr.sizeof_gr_complex*1, path+filename, False)
        self.data_sink.set_unbuffered(False)

        #self.correctiq_block = correctiq.correctiq()

        ##################################################
        # Connections
        ##################################################
        #self.connect((self.rtlsdr_antenna, 0), (self.correctiq_block, 0))
        #self.connect((self.correctiq_block, 0), (self.data_sink, 0))
        self.connect((self.rtlsdr_antenna, 0), (self.data_sink, 0))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.rtlsdr_antenna.set_sample_rate(self.samp_rate)

    def get_f0(self):
        return self.f0

    def set_f0(self, f0):
        self.f0 = f0
        self.rtlsdr_antenna.set_center_freq(self.f0, 0)
    
    ### Added sections ###
    def get_filename(self):
        return self.filename

    def set_filename(self, filename):
        self.filename = filename
        self.data_sink = blocks.file_sink(gr.sizeof_gr_complex*1, data_sink2.path+self.filename, False)
        self.data_sink.set_unbuffered(False)
        self.connect((self.rtlsdr_antenna, 0), (self.data_sink, 0))

def main(top_block_cls=data_sink2, options=None):

    #Acquire 1
    for i in range(fmin, fmax+1, 1):
      if(ykush_on):
        print("WARNING: Double acquisition is active, make sure you're running with sudo!\n")
        print("Activating hubs %s and %s.\n")%(ykush1, ykush2)
        args=['sudo', 'ykushcmd', '-u', ykush1]
        subprocess.Popen(args)
        args=['sudo', 'ykushcmd', '-u', ykush2]
        subprocess.Popen(args)
        time.sleep(2.5)
        args=['./'+scriptname]
        subprocess.Popen(args)
        time.sleep(2.5) ###
      tb = top_block_cls()
      freq=i*1e6
      print("Acquiring frequency %d MHz\n" % i)
      tb.set_f0(freq)
      tb.set_filename(test_name+str(i)+".dat")
      tb.start()
      time.sleep(1) ###
      tb.stop()
      tb.wait()
      #reset device to be able to start over
      del tb
      #dev = finddev(idVendor=0x0bda, idProduct=0x2838)
      #dev.reset()

      if(ykush_on):
        print("Deactivating hubs %s and %s.\n")%(ykush1, ykush2)
        args=['sudo', 'ykushcmd', '-d', ykush1]
        subprocess.Popen(args)
        args=['sudo', 'ykushcmd', '-d', ykush2]
        subprocess.Popen(args)
        time.sleep(1) ###
        tb = top_block_cls()
        tb.set_f0(freq)
        tb.set_filename(noise_name+str(i)+".dat")
        tb.start()
        time.sleep(1) ###
        tb.stop()
        tb.wait()
        #reset device to be able to start over
        del tb
        #dev = finddev(idVendor=0x0bda, idProduct=0x2838)
        #dev.reset()

if __name__ == '__main__':
    main()
