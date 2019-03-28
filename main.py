from image_manager import ImageManager
from sinogram_generator import SinogramGenerator
from sklearn.metrics import mean_squared_error
def error(tab1,tab2):
    return mean_squared_error(tab1, tab2)
import numpy as np

imageManager = ImageManager()
img = imageManager.readImage('Shepp_logan.jpg')
wyniki = []
dane = []
for i in range(10,15,10):
    print('-------' + str(i))
    sinogramGenrator = SinogramGenerator(img,300,240,1)
    # print("Min: {}, Max: {}".format(np.min(img), np.max(img)))
    # sinogram = sinogramGenrator.generate(img)
    # imageManager.showImage(sinogram, True, 'sinogram_bez_filtra')
    # imageManager.showImage(sinogramGenrator.revert(), True, 'reverted_bez_filtra')
    sinogramGenrator.withFilter = True
    sinogram = sinogramGenrator.generate(img)
    imageManager.showImage(sinogram, True, 'sinogram_z_filtrem')
    x = sinogramGenrator.revert()
    imageManager.showImage(x, True, 'reverted_z_fitrem')
    wyniki.append(error(x, img))
    dane.append(i)
    print(wyniki)

print(dane)
print(wyniki)
