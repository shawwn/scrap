#!/usr/bin/env python
#coding: utf-8
""" This work is licensed under a Creative Commons Attribution 3.0 Unported License.
    Frank Zalkow, 2012-2013 """

import pdb
import os
import sys
import numpy as np
from matplotlib import pyplot as plt
import scipy.io.wavfile as wav
from scikits.audiolab import Sndfile
from numpy.lib import stride_tricks
from moviepy.editor import AudioFileClip, VideoFileClip


cfg = {}
# cfg['bufsize'] = int(os.getenv('BUFSIZE','100000'))
# cfg['binsize'] = int(os.getenv('BINSIZE','4096'))
cfg['bufsize'] = int(os.getenv('BUFSIZE','200000'))
cfg['binsize'] = int(os.getenv('BINSIZE',str(2**16)))
cfg['verbose'] = os.getenv('VERBOSE')
cfg['fallback'] = 0

def np_abs(x):
    return np.abs(x)
    # return x

def load_media(filename,audio_buffersize=cfg['bufsize'],verbose=False):
    ext=os.path.splitext(filename)[1].lower()
    if ext in ['.wav', '.mp3', '.ogg', '.m4a']:
        return AudioFileClip(filename,buffersize=audio_buffersize)
    else:
        return VideoFileClip(filename,audio_buffersize=audio_buffersize,verbose=verbose)



def get_audio_signal(x,buffersize=cfg['bufsize']):
    x1 = x
    if cfg['verbose']:
        print('get_audio_signal(x, buffersize=%d)' % buffersize)
    if isinstance(x,str) or isinstance(x,unicode):
        x = load_media(x,audio_buffersize=buffersize)
        # pdb.set_trace()
    if isinstance(x,VideoFileClip):
        x = x.audio
    assert(isinstance(x,AudioFileClip))
    try:
        return x.fps, x.to_soundarray()
    except IOError as e:
        if cfg['verbose']:
            import traceback
            traceback.print_exc()
        cfg['fallback'] += 1
        if cfg['fallback'] == 1: #and buffersize == cfg['bufsize']:
            print('trying a smaller BUFSIZE...')
            #cfg['binsize'] /= 2
            cfg['bufsize'] /= 2
            return get_audio_signal(x1, buffersize=cfg['bufsize'])
        elif cfg['fallback'] == 2:
            print('trying BUFSIZE=80000...')
            cfg['bufsize'] = 80000
            return get_audio_signal(x1, buffersize=cfg['bufsize'])
        elif cfg['fallback'] == 3:
            print('trying BUFSIZE=80000 BINSIZE=2**12...')
            cfg['bufsize'] = 80000
            cfg['binsize'] = 2**12
            return get_audio_signal(x1, buffersize=cfg['bufsize'])
        else:
            print('falling back to stacker')
            # https://github.com/Zulko/moviepy/issues/281
            stacker = np.vstack if x.nchannels == 2 else np.hstack
            audio = stacker(x.iter_frames())
            return x.fps, audio

""" short time fourier transform of audio signal """
def stft(sig, frameSize, overlapFac=0.5, window=np.hanning):
    win = window(frameSize)
    hopSize = int(frameSize - np.floor(overlapFac * frameSize))

    # zeros at beginning (thus center of 1st window should be for sample nr. 0)
    samples = np.append(np.zeros(int(np.floor(frameSize/2.0))), sig)
    # cols for windowing
    cols = int(np.ceil( (len(samples) - frameSize) / float(hopSize)) + 1)
    # zeros at end (thus samples can be fully covered by frames)
    samples = np.append(samples, np.zeros(frameSize))

    frames = stride_tricks.as_strided(samples, shape=(cols, frameSize), strides=(samples.strides[0]*hopSize, samples.strides[0])).copy()
    frames *= win

    return np.fft.rfft(frames)

""" scale frequency axis logarithmically """
def logscale_spec(spec, sr=44100, factor=20.):
    timebins, freqbins = np.shape(spec)
    # pdb.set_trace()

    scale = np.linspace(0, 1, freqbins) ** factor
    scale *= (freqbins-1)/max(scale)
    scale = np.unique(np.round(scale))

    # create spectrogram with new freq bins
    newspec = np.complex128(np.zeros([timebins, len(scale)]))
    for i in range(0, len(scale)):
        if i == len(scale)-1:
            newspec[:,i] = np.sum(spec[:,int(scale[i]):], axis=1)
        else:
            newspec[:,i] = np.sum(spec[:,int(scale[i]):int(scale[i+1])], axis=1)

    # list center freq of bins
    allfreqs = np_abs(np.fft.fftfreq(freqbins*2, 1./sr)[:freqbins+1])
    freqs = []
    for i in range(0, len(scale)):
        if i == len(scale)-1:
            freqs += [np.mean(allfreqs[int(scale[i]):])]
        else:
            freqs += [np.mean(allfreqs[int(scale[i]):int(scale[i+1])])]

    return newspec, freqs

""" plot spectrogram"""
# def plotstft(audiopath, binsize=2**10, plotpath=None, colormap="jet", buffersize=cfg['bufsize']):
def plotstft(audiopath, binsize=cfg['binsize'], plotpath=None, colormap="jet", buffersize=cfg['bufsize']):
    # from audiolab import Sndfile
    # sound_file = Sndfile('test.w64', 'r')
    # signal = wave_file.read_frames(wave_file.nframes)

    # samplerate, samples = wav.read(audiopath)

    # clip = AudioFileClip(audiopath)
    # samplerate = clip.fps
    # samples = clip.to_soundarray(fps=samplerate)
    samplerate, samples = get_audio_signal(audiopath, buffersize=buffersize)

    s = stft(samples, binsize)

    sshow, freq = logscale_spec(s, factor=20.0, sr=samplerate)
    ims = 20.*np.log10(np_abs(sshow)/10e-6) # amplitude to decibel

    timebins, freqbins = np.shape(ims)

    plt.figure(figsize=(15, 7.5))
    plt.imshow(np.transpose(ims), origin="lower", aspect="auto", cmap=colormap, interpolation="bilinear")#"none")
    # # pdb.set_trace()
    plt.colorbar()

    plt.xlabel("time (s)")
    plt.ylabel("frequency (hz)")
    plt.xlim([0, timebins-1])
    plt.ylim([0, freqbins])

    import math
    # def lerp(x,y,t): return (y-x)*t+x
    # def wherebetween(a,b,x): return (x-a)/(b-a)
    # xlocs = [0.]
    # duration = len(samples)/float(samplerate)
    # mins = math.ceil(duration/60.0)
    # for i in xrange():

    # secs = len(samples)/float(samplerate)
    def format_time(duration):
        s,m = math.modf(duration / 60.0)
        s = int(s*60)
        return '%02d:%02d' % (m,s)
    xlocs = np.float32(np.linspace(0, timebins-1, 5))
    # plt.xticks(xlocs, ["%.02f" % l for l in ((xlocs*len(samples)/timebins)+(0.5*binsize))/samplerate])
    # xlocs = []
    # i = 0
    # while i <= len(samples):
    #   xlocs += [i*60.0*samplerate]
    #   i += 60*samplerate
    # xlocs += [len(samples)-1.0]
    # pdb.set_trace()

    plt.xticks(xlocs, [format_time(duration) for duration in ((xlocs*len(samples)/timebins)+(0.5*binsize))/samplerate])
    ylocs = np.int16(np.round(np.linspace(0, freqbins-1, 10)))
    plt.yticks(ylocs, ["%.02f" % freq[i] for i in ylocs])

    if plotpath:
        print('')
        print(plotpath)
        print('')
        plt.savefig(plotpath, bbox_inches="tight")
    else:
        plt.show()

    plt.clf()

if __name__ == '__main__':
    # for infile in sys.argv[1:]:
    #     outfile='%s.png' % infile
    #     print '%s -> %s' % (infile, outfile)
    #     ext=os.path.splitext(infile)[1]
    #     if ext == 'm4a':
    #         wavfile=infile
    #     elif ext == 'wav':
    #         wavfile=infile
    #     else:
    #         wavfile='specpy-input.wav'
    #         os.system("faad '%s' -o '%s'" % (infile, wavfile))
    #     plotstft(wavfile, plotpath=outfile)
    #     os.system("rm -f specpy-input.wav")

    for infile in sys.argv[1:]:
        outfile = '%s.png' % infile
        print '%s -> %s' % (infile, outfile)
        try:
            plotstft(infile, plotpath=outfile)
        except e:
            print("Error:", sys.exc_info()[0])
            pdb.set_trace()
