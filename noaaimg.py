#! Laba-horoshaya №2
#! (C) Made with love to informatics by:
#! Semyonova Alyona and Osipov Egor
#! Made in 230 palata 

#! We used a few parts of code from this absolutly brilliant pages:
#!  https://habr.com/ru/post/535206/
#!  https://github.com/zacstewart/apt-decoder

import matplotlib.pyplot as plt
import scipy.io.wavfile  as wav
import scipy.signal      as signal
import numpy             as np
import scipy
import sys

from PIL        import Image

class wav_to_png(object):

    def __init__(self, filename='out.wav'):
        """ Gets a self.signal data from filename wav file. Ignores some usless information in the end of self.signal """
        (rate, self.signal) = wav.read(filename)

        assert rate == 20800, "Use resample.sh to resample %s to rate 20800" % (filename)
        
        truncate = 20800 * int(len(self.signal) // 20800)
        self.signal = self.signal[:truncate]

    def hilbert(self, data):
        """ ADM """
        analytical_signal = signal.hilbert(data)
        amplitude_envelope = np.abs(analytical_signal)
        return amplitude_envelope

    def sync(self, data):
        """ Find syncs and create matrix from data """
        syncA = [0, 128, 255, 128]*7 + [0]*7

        peaks = [(0, 0)]

        mindistance = 2000

        signalshifted = [x-128 for x in data]
        syncA = [x-128 for x in syncA]
        for i in range(len(data)-len(syncA)):
            corr = np.dot(syncA, signalshifted[i : i+len(syncA)])

            if i - peaks[-1][0] > mindistance:
                peaks.append((i, corr))

            elif corr > peaks[-1][1]:
                peaks[-1] = (i, corr)

        matrix = []
        for i in range(len(peaks) - 1):
            matrix.append(data[peaks[i][0] : peaks[i][0] + 2080])

        return np.array(matrix)


    def lum(self, data):
        """ Transfer data to luminance data. All values become integers from 0 to 255 """
        maximum = max(data)
        minimum = min(data)

        a = 255/(maximum - minimum)
        b = -a*minimum
        for i in range(len(data)):
            data[i] = a*data[i] + b

        return data

    def decode(self, outfile='output.png'):
        """ Step by step calls needed funcs """
        data = self.hilbert(self.signal)
        data = data.reshape(int(len(data) // 5), 5)
        data = self.lum(data[:, 2])

        result = self.sync(data)

        image = Image.fromarray(result)
        image = image.convert('RGB')
        image.save(outfile)

if __name__ == "__main__":

    if len(sys.argv) > 1:
        converter = wav_to_png(sys.argv[0])
    else:
        converter = wav_to_png()

    if len(sys.argv) > 2:
        converter.decode(sys.argv[1])
    else:
        converter.decode()
