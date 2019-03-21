from skimage import data, io
from skimage.color import rgb2gray
from skimage.transform import resize
import matplotlib.pyplot as plt

class ImageManager:

    def readImage(self, path):
        img = data.imread(path)
        img = rgb2gray(img)
        return resize(img, (300, 300), anti_aliasing=True)

    def showImage(self, img):
        io.imshow(img, cmap=plt.cm.gray)
        io.show()