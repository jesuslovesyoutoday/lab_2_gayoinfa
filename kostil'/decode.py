from PIL import Image
import numpy as np

im = Image.open('image2.png')
a = np.asarray(im)

np.savetxt('image_mit.txt', a, fmt = '%d')


