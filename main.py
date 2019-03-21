from image_manager import ImageManager
from sinogram_generator import SinogramGenerator

imageManager = ImageManager()
img = imageManager.readImage('tomograf-zdjecia/Kwadraty2.jpg')
imageManager.showImage(img)
sinogramGenrator = SinogramGenerator(img)
sinogram = sinogramGenrator.generate(img)
imageManager.showImage(sinogram)
imageManager.showImage(sinogramGenrator.revert())
