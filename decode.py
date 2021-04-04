#! Laba-horoshaya №2
#! (C) Made with love to informatics by:
#! Semyonova Alyona and Osipov Egor
#! Made in 230 palata 

#! We used a few parts of code from this brilliant pages:
#!  https://habr.com/ru/post/535206/
#!  https://github.com/zacstewart/apt-decoder

import matplotlib.pyplot as plt
import scipy.io.wavfile  as wav
import scipy.signal      as signal
import numpy             as np
import scipy

from statistics import mean
from PIL        import Image

def resample(data, fs):
    resample = 5 #int(11025/4159.8)
    fs = fs//resample
    data = data[::resample]
    return data, fs

def hilbert(data):
    analytical_signal = signal.hilbert(data)
    amplitude_envelope = np.abs(analytical_signal)
    return amplitude_envelope
    
def _reshape(data):
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

def impulse(data, it):
    fo = open("synh_indexes.dat", "w")
    imp = False
    k = 1
    impulse = [78, 247, 255, 88, 33, 253, 255, 65, 63, 235, 
               253, 47, 62, 255, 240, 78, 42, 230, 255, 57, 
               65, 242, 255, 60, 55, 255, 232]
    result = []
    for i in range(len(impulse)):
        result.append(0)
    while not(imp) and it < len(data) - len(impulse):
        for i in range(len(impulse)):
            result[i] = abs(data[it + i] - impulse[i])
        res = sum(result)
        if res < 2368.75:
            fo.write(str(it) + "\n")
            it += 2070
        it += 1

    fo.close()

    
def get_impulsed_egor_loh_data(data, fs):
    # impulse(data, 0)
    
    fi = open("synh_indexes.dat", "r")
    indexes = list(map(int, fi.readlines()))

    impulsed_data = []

    for i in range(len(indexes)):
        impulsed_data.append(data[indexes[i]:indexes[i] + 2080])

    fo = open("impulsed_data.dat", "w")
    
    for i in impulsed_data:
        for j in i:
            fo.write(str(int(j)) + " ")
        fo.write("\n")

    for i in impulsed_data:
        print(len(i))

    graph(impulsed_data[0:len(impulsed_data) - 1], fs)
    fi.close()
    fo.close()


""" We cannot delete this, because of our love to debug :::))) """
def matrix(data, fs):
    l = []
    ma = []

    new_fs = int(fs * 0.5)

    #errors = impulse(data)
    for i in range (int(len(data)/new_fs)):
        for j in range(new_fs):
            l.append(data[i*new_fs + j])
        ma.append(l)
        l = []
    print("Matrix final length: ", len(ma))
    return ma


def lum(data_am):
    maximum = max(data_am)
    minimum = min(data_am)

    a = 255/(maximum - minimum)
    b = -a*minimum
    for i in range(len(data_am)):
        data_am[i] = a*data_am[i] + b

    return data_am

def graph(data_am, fs):
    new_fs = 2080# fs
    w, h = new_fs, len(data_am)
    image = Image.new('RGB', (w, h))

    px, py = 0, 0
    for i in range(len(data_am)):
        for j in range(new_fs):
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

    # mage = image.resize((w, 4*h))
    # plt.imshow(image)
    # plt.show()
    # plt.imsave('image.png',image)
    image.save('image.png')

def print_shit_in_shit(data_am):
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
    fs, data = wav.read('out.wav')
    print("Rate:", fs)

    RATE = 20800
    truncate = RATE * int(len(data) // RATE)
    data = data[:truncate]
    print(len(data))
    data_am = hilbert(data)
    data_am = data_am.reshape(int(len(data_am) // 5), 5)
    data_am = lum(data_am[:, 2])

    result = _reshape(data_am)
    
    image = Image.fromarray(result)
    image = image.convert('RGB')
    image.save("./result/output.png")

