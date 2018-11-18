#!/usr/bin/env python2
"""Frequency processing script."""

import struct
import os
from scipy.fftpack import fft, fftshift, fftfreq
from scipy.signal import blackmanharris, welch, spectrogram, csd
from detect_peaks import detect_peaks
import numpy as np
import matplotlib.pyplot as plt
import math
import types
import datetime as dt
import argparse

__author__ = "Valerio Lanieri"
__version__ = "1.0.0"
__license__ = "MIT"

def peakscannerdb(yaxis, th=0, export=False, xaxis=None, exportname=""):
  """Function used to scan a power spectrum for peaks"""
  yaxis=10*np.log10(yaxis)
  peaks=detect_peaks(yaxis, mph=th, threshold=1, kpsh=True, mpd=0)
  if(export):
    np.savetxt(exportname, np.column_stack([xaxis[peaks], yaxis[peaks]]), '%.5f', header="f[MHz]\tP[dB]", comments='#')
  return peaks

def ldmesh(xaxis, yaxis, zaxis, center_freq=0, plotnum=""):
  """This function loads a matplotlib.pyplot figure with color mesh data which can be later plotted"""
  plt.pcolormesh(xaxis, yaxis, zaxis)
  plt.title("Spectrogram "+plotnum+str(center_freq)+" MHz")
  plt.xlabel("Time [s]")
  plt.ylabel("Frequency [MHz]")
  plt.grid(True)

def ldplotdb(xaxis, yaxis, center_freq=0, plotnum="", peaks=[]):
  """This function loads a matplotlib.pyplot figure with xaxis and yaxis data which can later be plotted"""
  yaxis=10*np.log10(yaxis)
  if(len(peaks)!=0):
    plt.plot(xaxis[peaks], yaxis[peaks], 'ro')
  plt.plot(xaxis, yaxis)
  plt.title("FFT "+plotnum+str(center_freq)+" MHz")
  plt.xlabel("Frequency [MHz]")
  plt.ylabel("Power [dB]")
  plt.grid(True)

def ldcomplex(filename):
  """This function stores data coming from a raw byte file into an array of complex numbers"""
  size=os.path.getsize(filename)/4 #number of floats inside filename
  file=open(filename, "rb")
  tmp=struct.unpack('f'*size, file.read(size*4))
  data=map(lambda r,i : complex(r,i), tmp[::2], tmp[1::2])
  file.close()
  return data

def main():
  ### Parse commandline arguments
  parser = argparse.ArgumentParser(description='Processes time domain data to perform frequency domain analysis')
  parser.add_argument('-p', '--path', metavar='path', default="./data", help='define path of input files')
  parser.add_argument('-f1', '--filename1', metavar='filename', default="test", help='set filename for test dump')
  parser.add_argument('-f2', '--filename2', metavar='filename', default="bg", help='set filename for background dump')
  parser.add_argument('-fs', '--fsampling', metavar='N', type=float, default=2e6, help='set sampling frequency of input data')
  parser.add_argument('-n', '--fftsize', metavar='N', type=int, default=16383, help='set FFT size')
  parser.add_argument('-na', '--nall', action='store_false', help='disabilitates overall frequency plot')
  parser.add_argument('-s', '--step', action='store_true', help='abilitates step by step frequency plot')
  parser.add_argument('-d', '--diff', action='store_true', help='performs difference between spectrum with board and spectrum without board')
  parser.add_argument('-g', '--spg', action='store_true', help='show spectrogram')
  parser.add_argument('-P', '--peaks', action='store_true', help='abilitates peak search')
  parser.add_argument('-t', '--Pth', metavar='dB', type=int, default=-90, help='set power threshold for peak search (in dB) - default: -90 ')
  parser.add_argument('-e', '--epeaks', action='store_true', help='exports peak search, -P option must be selected')
  parser.add_argument('-fP', '--fpeaks', metavar='filename', default="scan", help='set filename for peak export (default: scan)')
  parser.add_argument('-w', '--efft', action='store_true', help='exports data inside compressed .npz files')
  parser.add_argument('-l', '--load', action='store_true', help='load data from compressed .npz files')
  parser.add_argument('-fw', '--fftname', metavar='filename', default="fft_export", help='choose filename for FFT export/load (default: fft_export)')
  parser.add_argument('-fg', '--spgname', metavar='filename', default="spg_export", help='choose filename for spectrogram export/load (default: spg_export)')
  parser.add_argument('frequency', metavar='f', type=int, nargs=2, default=[26, 28], help='frequency range')

  args = parser.parse_args()

  ### Options
  export_fft=args.efft
  load_fft=args.load
  diff=args.diff
  find_peaks=args.peaks
  export_peaks=args.epeaks
  plot_step=args.step
  plot_all=args.nall
  show_spectrogram=args.spg

  ### Parameters
  fmin=args.frequency[0] #minimum center frequency in MHz (MIN:25)
  fmax=args.frequency[1] #maximum center frequency in MHz (MAX: 1000)
  if fmax<fmin:
    print("Error: fmin larger than fmax")
    quit()
  path=args.path+"/" #path of acquired data
  data_filename=args.filename1
  diff_filename=args.filename2 #difference filename
  Pth=args.Pth #set power threshold in negative dB
  peaks_filename=args.fpeaks #filename of peaks export
  fft_filename=args.fftname
  Fs=args.fsampling #data sampling frequency
  dT=1/Fs #sampling rate
  fft_size=args.fftsize #FFT size
  spg_filename=args.spgname

  f=fftfreq(fft_size, d=dT) #x-axis for FFT
  f=fftshift(f)
  peaks=peaks1=peaks2=[]
  if(export_peaks):
    suffix=str(dt.datetime.now()).replace(" ", "_").replace(":", "").replace("-", "")[:-7]+".txt"
    scan=path+peaks_filename+"_"+suffix #path of scan output
    scan1=path+peaks_filename+"1_"+suffix #path of scan output
    scan2=path+peaks_filename+"2_"+suffix #path of scan output
  else:
    scan=""
    scan1=""
    scan2=""

  if(load_fft==False):
    for f0 in range (fmin, fmax+1, int(Fs/1e6)):
      #### the step is used to avoid repetitions (default Fs is 2e6) ####
      ### Open file 1
      data=ldcomplex(path+data_filename+str(f0)+".dat")
      ### FFT spectrum, Welch average method
      if(diff):
        ### Open file 2
        data2=ldcomplex(path+diff_filename+str(f0)+".dat")
        ### Compute difference between averaged FFts
        _, P1 = welch(data, Fs, 'hanning', fft_size, None, None, 'constant', True, 'spectrum')
        _, P2 = welch(data2, Fs, 'hanning', fft_size, None, None, 'constant', True, 'spectrum')
        P1=fftshift(P1)
        P2=fftshift(P2)
        P=np.square(np.sqrt(P1)-np.sqrt(P2))
        if(show_spectrogram):
          fsg, tsg, Sxx1 = spectrogram(data, Fs, scaling='spectrum', nperseg=1024)
          _, _, Sxx2 = spectrogram(data2, Fs, scaling='spectrum', nperseg=1024)
          Sxx = np.square(np.sqrt(Sxx1)-np.sqrt(Sxx2))
      else:
        _, P = welch(data, Fs, 'hanning', fft_size, None, None, 'constant', True, 'spectrum')
        P=fftshift(P)
        if(show_spectrogram):
          fsg, tsg, Sxx = spectrogram(data, Fs, scaling='spectrum', nperseg=1024)
      if(plot_all or export_fft or export_peaks):
      ## APPEND DATA FOR GLOBAL PLOT
        if f0==fmin:
          f_global=f/1e6+f0
          P_global=P
          if(show_spectrogram):
            fsg_global=fftshift(fsg/1e6+f0)
            Sxx_global=fftshift(Sxx)
          if(diff):
            P1_global=P1
            P2_global=P2
            if(show_spectrogram):
              Sxx1_global=fftshift(Sxx1)
              Sxx2_global=fftshift(Sxx2)
        else:
          f_global=np.append(f_global, f/1e6+f0)
          P_global=np.append(P_global, P)
          if(show_spectrogram):
            fsg_global=np.append(fsg_global, fftshift(fsg/1e6+f0))
            Sxx_global=np.concatenate((Sxx_global, fftshift(Sxx)), axis=0)
          if(diff):
            P1_global=np.append(P1_global, P1)
            P2_global=np.append(P2_global, P2)
            if(show_spectrogram):
              Sxx1_global=np.concatenate((Sxx1_global, fftshift(Sxx1)), axis=0)
              Sxx2_global=np.concatenate((Sxx2_global, fftshift(Sxx2)), axis=0)
      ### PLOT (f0)
      if(plot_step):
        f1=plt.figure(1)
        if(diff):
          plt.subplots_adjust(left=0.12, bottom=0.08, right=0.95, top=0.93, wspace=0.28, hspace=0.34)
          plt.subplot(2,2,1)
          if(find_peaks):
            peaks1=peakscannerdb(P1, Pth, export=False)
            peaks2=peakscannerdb(P2, Pth, export=False)
          ldplotdb(f/1e6+f0, P1, f0, "1 ", peaks1)
          plt.subplot(2,2,2)
          ldplotdb(f/1e6+f0, P2, f0, "2 ", peaks2)
          plt.subplot(2,1,2)
        if(find_peaks):
          peaks=peakscannerdb(P, Pth, export=False)
        ldplotdb(f/1e6+f0, P, f0, "", peaks)
        plt.ion() #interactive plot
        plt.show()
        if(show_spectrogram):
          f2=plt.figure(2)
          if(diff):
            plt.subplots_adjust(left=0.12, bottom=0.08, right=0.95, top=0.93, wspace=0.28, hspace=0.34)
            plt.subplot(2,2,1)
            ldmesh(tsg, fftshift(fsg/1e6+f0), fftshift(Sxx1), f0, "1 ")
            plt.subplot(2,2,2)
            ldmesh(tsg, fftshift(fsg/1e6+f0), fftshift(Sxx2), f0, "2 ")
            plt.subplot(2,1,2)
          ldmesh(tsg, fftshift(fsg/1e6+f0), fftshift(Sxx), f0)
          plt.show()
        raw_input("Press any key to continue...")
        plt.close(f1)
        if(show_spectrogram):
          plt.close(f2)
  else:
    fft_dict=np.load(path+fft_filename+".npz")
    f_global=fft_dict['f']
    P_global=fft_dict['P']
    if(show_spectrogram):
      spg_dict=np.load(path+spg_filename+".npz")
      tsg=spg_dict['tsg']
      fsg_global=spg_dict['fsg']
      Sxx_global=spg_dict['Sxx']
    if(diff):
      fft_dict=np.load(path+fft_filename+"_P1"+".npz")
      P1_global=fft_dict['P']
      fft_dict=np.load(path+fft_filename+"_P2"+".npz")
      P2_global=fft_dict['P']
      if(show_spectrogram):
        spg_dict=np.load(path+spg_filename+"_S1"+".npz")
        Sxx1_global=spg_dict['Sxx']
        spg_dict=np.load(path+spg_filename+"_S2"+".npz")
        Sxx2_global=spg_dict['Sxx']

  if((plot_all and find_peaks) or export_peaks):
    peaks=peakscannerdb(P_global, Pth, export_peaks, f_global, scan)
    if(diff):
      peaks1=peakscannerdb(P1_global, Pth, export_peaks, f_global, scan1)
      peaks2=peakscannerdb(P2_global, Pth, export_peaks, f_global, scan2)

  if(export_fft and not(load_fft)):
    np.savez_compressed(path+fft_filename, f=f_global, P=P_global)
    if(show_spectrogram):
      np.savez_compressed(path+spg_filename, tsg=tsg, fsg=fsg_global, Sxx=Sxx_global)
    if(diff):
      np.savez_compressed(path+fft_filename+"_P1", f=f_global, P=P1_global)
      np.savez_compressed(path+fft_filename+"_P2", f=f_global, P=P2_global)
      if(show_spectrogram):
        np.savez_compressed(path+spg_filename+"_S1", tsg=tsg, fsg=fsg_global, Sxx=Sxx1_global)
        np.savez_compressed(path+spg_filename+"_S2", tsg=tsg, fsg=fsg_global, Sxx=Sxx2_global)

  ### PLOT (from fmin-Fs/2 to fmax+Fs/2)
  if(plot_all):
    f1=plt.figure(1)
    if(diff):
      plt.subplots_adjust(left=0.12, bottom=0.08, right=0.95, top=0.93, wspace=0.28, hspace=0.34)
      plt.subplot(2,2,1)
      ldplotdb(f_global, P1_global, (fmax+fmin)/2, "1 ", peaks1)
      plt.subplot(2,2,2)
      ldplotdb(f_global, P2_global, (fmax+fmin)/2, "2 ", peaks2)
      plt.subplot(2,1,2)
    ldplotdb(f_global, P_global, (fmax+fmin)/2, "", peaks)
    plt.ion() #interactive plot
    plt.show()
    if(show_spectrogram):
      f2=plt.figure(2)
      if(diff):
        plt.subplots_adjust(left=0.12, bottom=0.08, right=0.95, top=0.93, wspace=0.28, hspace=0.34)
        plt.subplot(2,2,1)
        ldmesh(tsg, fsg_global, Sxx1_global, (fmax+fmin)/2, "1 ")
        plt.subplot(2,2,2)
        ldmesh(tsg, fsg_global, Sxx2_global, (fmax+fmin)/2, "2 ")
        plt.subplot(2,1,2)
      ldmesh(tsg, fsg_global, Sxx_global, (fmax+fmin)/2)
      plt.show()
    raw_input("Press any key to close...")
    plt.close(f1)
    if(show_spectrogram):
      plt.close(f2)

if __name__ == '__main__':
  main()

# Previous method to compute difference
        #minlen=min([len(data), len(data2)])
        #w=blackmanharris(fft_size)
        #mean=np.mean(data)
        #data=[x-mean for x in data] # Remove DC offset
        #mean=np.mean(data2)
        #data2=[x-mean for x in data2] # Remove DC offset
        #for i in range(0, int(math.floor(minlen/fft_size))):
        #    fft1=fft([x*y for x,y in zip(data[i*fft_size/2:i*fft_size/2+fft_size],w)])/math.sqrt(fft_size)
        #     fft2=fft([x*y for x,y in zip(data2[i*fft_size/2:i*fft_size/2+fft_size],w)])/math.sqrt(fft_size)
        #     if i==0:
        #         avg1=np.square(np.absolute(fft1))
        #         avg2=np.square(np.absolute(fft2))
        #         avg=np.square(np.absolute(fft1)-np.absolute(fft2))
        #     else:
        #         avg1=avg1+np.square(np.absolute(fft1))
        #         avg2=avg2+np.square(np.absolute(fft2))
        #         avg=avg+np.square(np.absolute(fft1)-np.absolute(fft2))
        #P1=fftshift(avg1/(1+i))
        #P2=fftshift(avg2/(1+i))
        #P=fftshift(avg/(1+i))
        ##P=fftshift(np.square((np.sqrt(avg1)-np.sqrt(avg2)))/(i+1))
