from image_manager import ImageManager
from sinogram_generator import SinogramGenerator

imageManager = ImageManager()
img = imageManager.readImage('tomograf-zdjecia/Shepp_logan.jpg')
sinogramGenrator = SinogramGenerator(img)
# sinogram = sinogramGenrator.generate(img)
# imageManager.showImage(sinogram, True, 'sinogram_bez_filtra')
# imageManager.showImage(sinogramGenrator.revert(), True, 'reverted_bez_filtra')
sinogramGenrator.withFilter = True
sinogram = sinogramGenrator.generate(img)
imageManager.showImage(sinogram, True, 'sinogram_z_filtrem')
imageManager.showImage(sinogramGenrator.revert(), True, 'reverted_z_fitrem')
