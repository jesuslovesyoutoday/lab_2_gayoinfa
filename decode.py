#! Laba-huyaba №2
#! (C) Made with love to gays and informatics by:
#! Semyonova Alyona and Osipov Egor
#! Made in 230 palata 

#! We used a few parts of code from this brilliant habr page:
##  habr.com/ru/535206

import scipy.io.wavfile as wav
import scipy.signal as signal
import numpy as np
import matplotlib.pyplot as plt
from statistics import mean

from PIL import Image

fs, data = wav.read('signal.WAV')

DATA_LEN = len(data)
print(DATA_LEN)

#plt.figure(figsize=(12,4))
#plt.plot(data)
#plt.show()

def resample(data, fs):
    resample = int(11025/4160)
    data = data[::resample]
    fs = fs//resample
    return data, fs

def hilbert(data):
    analytical_signal = signal.hilbert(data)
    amplitude_envelope = np.abs(analytical_signal)
    return amplitude_envelope

def impulse(data, it):
    errors = 0;
    imp = False
    impulse = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
    while not(imp):
        if (data[it] == impulse[0]):
            for j in impulse:
                if (data[it] == j):
                    print("NO")
                    imp = True
                    it += 1
                else:
                    print("YES")
                    imp = False
                    break
        it += 1
    return data[(it-10):(it + 2080)];
    
# <it> is @param for iteration in impulse() func
# it is made -2000 because we want more "ApTiMiSaTiOn"
# it = -2000

def get_impulsed_egor_loh_data(data):
    impulsed_data = []
    
    it = -2000
    while it < DATA_LEN:
        it += 2000
        print(it)
        impulsed_data.append(impulse(data, it))

    return impulsed_data


""" We cannot delete this, because of our love to gays in informatics :::))) """
def matrix(data):
    l = []
    ma = []

    #errors = impulse(data)
    for i in range (int(len(data)/2080)):
        for j in range(2080):
            l.append(data[i*2080 + j])
        ma.append(l)
        l = []
    print("Matrix final length: ", len(ma))
    return ma


def lum(data_am):
    maximum = max(data_am)
    minimum = min(data_am)

    print(maximum, minimum)
    a = 255/(maximum - minimum)
    b = -a*minimum
    for i in range(len(data_am)):
        data_am[i] = a*data_am[i] + b

    return data_am

def graph(data_am, fs):
    
    w, h = 2080, len(data_am)
    image = Image.new('RGB', (w, h))

    px, py = 0, 0
    for i in range(len(data_am)):
        for j in range(2080):
            lum = int(data_am[i][j])
            image.putpixel((px, py), (lum, lum, lum))
            px += 1
            if px >= w:
                if (py % 50) == 0:
                    print(f'Line saved {py} of {h}')
                px = 0
                py += 1
                if py >= h:
                    break

    mage = image.resize((w, 4*h))
    plt.imshow(image)
    plt.show()
    #plt.imsave('image.png',image)

def print_shit_in_shit():
    k = 0
    for i in range(10000):
        if (data_am[i] > 200):
            print("Start of synh: ", i)
            for j in range(40):
                print(int(data_am[i + j]), end=' ')
                k += 1
                if k % 5 == 0:
                    print()
            print()
            print()
        i += 40
    print()


if __name__ == "__main__":
    data, fs = resample(data, fs)
    data_am = hilbert(data)

    data_am = lum(data_am)
