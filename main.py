from image_manager import ImageManager
from sinogram_generator import SinogramGenerator

imageManager = ImageManager()
img = imageManager.readImage('Shepp_logan.jpg')
sinogramGenrator = SinogramGenerator(img)
sinogram = sinogramGenrator.generate(img)
imageManager.showImage(sinogram)
imageManager.showImage(sinogramGenrator.revert())
