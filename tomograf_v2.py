from skimage import data, io, filters, exposure, img_as_ubyte, img_as_float
from skimage.color import rgb2gray, hsv2rgb, rgb2hsv
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


def normalize(x):
    max = 0
    for i in x:
        for a in i:
           if a > max:
               max = a
    print(max)
    for i in range(0, len(x)):
        for a in range(0, len(x[0])):
            x[i, a] = int(x[i, a] / max)
    return x


def prosta(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    dx = x2 - x1
    dy = y2 - y1
    obrot = abs(dy) > abs(dx)

    if obrot:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
    e = int(dx * 1/2)
    if y1 < y2 :
        krok = 1
    else:
        krok = -1
    dx = x2 - x1
    dy = y2 - y1
    prosta = []
    for i in range(int(x1), int(x2 + 1)):
        if obrot:
            prosta.append([y1, i])
        else:
            prosta.append([i, y1])
        e -= abs(dy)
        if e < 0:
            y1 += krok
            e +=dx
    return prosta


def line(x, y):
    A = x[1] - y[1]
    B = y[0] - x[0]
    C = x[0]*y[1] - y[0]*x[1]
    return A, B, -C


def intersection_points(p1, p2):
    L1 = line(p1[0], p1[1])
    L2 = line(p2[0], p2[1])
    D = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    return int(Dx/D), int(Dy/D) #TODO wystarczy int?


def emiter(r, alfa):
    x = r * np.cos(np.deg2rad(alfa))
    y = r * np.sin(np.deg2rad(alfa))
    return [x, y]


def detect_side(point, img_shape):#TODO trzeba poprawic zeby srodek byl w srodku okregu
    if point[0] <= 0:
        return [[0, img_shape[1] - 1], [0, 0]]
    elif point[0] >= img_shape[0]:
        return [[img_shape[0] - 1, img_shape[1] - 1], [img_shape[0] - 1, 0]]
    elif point[1] < 0:
        return [[0, 0], [0, img_shape[0] - 1]]
    else:
        return [[img_shape[0] - 1, img_shape[1] - 1], [0, img_shape[1] - 1]]



def detektory_na_okregu(r, alfa, l, n):
    detektory = []
    for i in range(0, n):
        arg = alfa + np.pi - l/2 + i * (l/(n - 1))
        arg = np.deg2rad(arg)
        x = r * np.cos(arg)
        y = r * np.sin(arg)
        detektory.append([x, y])
    return detektory


def detektory_na_prostokacie(detektory_na_okregu, center, img_shape):
    for nr, i in enumerate(detektory_na_okregu):
        point2 = detect_side(i, img_shape)
        detektory_na_okregu[nr] = intersection_points([i, center], point2)
    return detektory_na_okregu

def emiter_na_prostokacie(p, center, img_shape):
    #TODO jakos ogarnac zeby brac odpowiednia krawedz prostokata
    point2 = detect_side(p, img_shape)
    return intersection_points([p, center], point2)




def make_sinogram(n, l, alfa, img, r, center):
    ilosc = int(360 / alfa)
    sinogram = np.zeros((n, ilosc))
    for i in range(0, ilosc):
        print(str(i) + "------")
        alfa = alfa * i
        emiter_p = emiter(r, alfa)
        print(emiter_p)
        emiter_p = emiter_na_prostokacie(emiter_p, center, img.shape)
        detektory = detektory_na_okregu(r, alfa, l, n)
        print(detektory)
        print("...........")
        detektory = detektory_na_prostokacie(detektory, center, img.shape)
        print(emiter_p)
        print(detektory)
        print("........")
        for nr, e in enumerate(detektory):
            value = 0
            linia = prosta(emiter_p, e)
            for q in linia:
                value += img[q[0], q[1]]
            sinogram[nr, i] = value
    return sinogram


n = 3 #ilosc detektorow
l = 50 #kat rozlozenia detektorow
alfa = 1 #kat przesunicia
img = data.imread('CT_ScoutView.jpg')
img = rgb2gray(img)

print(img.shape)
center = [img.shape[0]/2, img.shape[1]/2]
r = np.sqrt(pow(img.shape[0], 2) + pow(img.shape[1], 2)) / 2
print(r)

sinogram = make_sinogram(n, l, alfa, img, r, center)
print(sinogram)


