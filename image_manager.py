from skimage import data, io
from skimage.color import rgb2gray
from skimage.transform import resize
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

class ImageManager:

    def readImage(self, path):
        img = data.imread(path)
        img = rgb2gray(img)
        # return img
        # print("Min: {}, Max: {}".format(np.min(img), np.max(img)))
        return resize(img, (300, 300), anti_aliasing=True)

    def showImage(self, img, save, name):
        io.imshow(img, cmap=plt.cm.gray)
        if save == True:
            plt.savefig(name+str(datetime.now())+'.jpg')
        io.show()