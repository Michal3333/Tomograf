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
    # print("promien: {}".format(r))
    x = r * np.cos(np.deg2rad(alfa))
    y = r * np.sin(np.deg2rad(alfa))
    return [int(x), int(y)]


def detect_side(point, img_shape):#TODO trzeba poprawic zeby srodek byl w srodku okregu
    if point[0] <= 0:
        return [[0, img_shape[1] - 1], [0, 0]]
    elif point[0] >= img_shape[0]:
        return [[img_shape[0] - 1, img_shape[1] - 1], [img_shape[0] - 1, 0]]
    elif point[1] < 0:
        return [[0, 0], [0, img_shape[0] - 1]]
    else:
        return [[img_shape[0] - 1, img_shape[1] - 1], [0, img_shape[1] - 1]]


# r - promień okręgu
# alfa - kąt przesunięcia emittera
# 1 - ???
# n - liczba detektorów
def detektory_na_okregu(r, alfa, l, n):
    detektory = []
    for i in range(0, n):
        arg = np.deg2rad(alfa) + np.pi - np.deg2rad(l)/2 + i * (np.deg2rad(l)/(n - 1))
        # arg = np.deg2rad(arg)
        x = r * np.cos(arg)
        y = r * np.sin(arg)
        detektory.append([int(x), int(y)])
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
    test = np.zeros((img.shape[0]+r, img.shape[1]+r))
    ilosc = int(360 / alfa)
    sinogram = np.zeros((n, ilosc))
    max_x = img.shape[0]
    max_y = img.shape[1]
    for i in range(0, ilosc):
        # print(str(i) + "------")
        alfa = i
        # print("alfa: {}".format(alfa))
        emiter_p = emiter(r, alfa)
        # print("Emitter: {}".format(emiter_p))
        # emiter_p = emiter_na_prostokacie(emiter_p, center, img.shape)
        detektory = detektory_na_okregu(r, alfa, l, n)
        # print("Detektory: {}".format(detektory))
        # detektory = detektory_na_prostokacie(detektory, center, img.shape)
        # print(emiter_p)
        # print(detektory)
        for nr, e in enumerate(detektory):
            value = 0
            linia = prosta(emiter_p, e)
            # print("emiter: {}".format(emiter_p))
            # print("detektor: {}".format(e))
            # print("linia: {}".format(linia))
            count = 0
            for q in linia:
                a = 0
                b = 0
                if q[0] <= max_x and q[0] >=0 and q[1] <= max_y and q[1] >=0:
                    a = q[0]
                    b = q[1]
                    count += 1
                    amount[a, b] += 1
                    value += img[a, b]
            if count > 0:
                value = value / count
            sinogram[nr, i] += value
            test[emiter_p[0]+r, emiter_p[1]+r] = 1
    
    return sinogram, test

def transoform_to_img(sinogram, alfa, r, l, n):
    ilosc = int(360 / alfa)
    img = np.zeros((n, ilosc))
    max_x = img.shape[0]
    max_y = img.shape[1]
    for i in range(0, ilosc):
        alfa = i
        emiter_p = emiter(r, alfa)
        detektors = detektory_na_okregu(r, alfa, l, n)
        for nr, e in enumerate(detektors):
            # print(len(detektors))
            value = 0
            linia = prosta(emiter_p, e)
            # print("emiter: {}".format(emiter_p))
            # print("detektor: {}".format(e))
            # print("linia: {}".format(linia))
            # print(img.shape)
            for q in linia:
                a = 0
                b = 0
                if q[0] <= max_x and q[0] >=0:
                    a = q[0] - 1
                if q[1] <= max_y and q[1] >=0:
                    b = q[1] - 1
                img[a, b] += sinogram[nr, alfa]
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if amount[i, j] > 0:
                print("img: {}, amount: {}".format(img[i, j], amount[i, j]))
                img[i, j] = img[i, j] / amount[i, j]
    return img

n = 60 #ilosc detektorow
l = 60 #kat rozlozenia detektorow
alfa = 1 #kat przesunicia
img = data.imread('ct-scan.jpg')
img2 = img
img = rgb2gray(img)
amount = np.zeros(img.shape)
print(img.shape)
center = [img.shape[0]/2, img.shape[1]/2]
r = int(np.sqrt(pow(center[0], 2) + pow(center[1], 2)) / 2)
print(r)

sinogram, test = make_sinogram(n, l, alfa, img, r, center)
print(test)
# io.imshow(abs(plot_image), cmap='gray_r')
# plt.show() 
# sinogram = sinogram / 255
io.imshow(sinogram, cmap=plt.cm.gray)
io.show()

io.imshow(test, cmap=plt.cm.gray)
io.show()

output = transoform_to_img(sinogram, alfa, r, l, n)
print(output)
io.imshow(output, cmap=plt.cm.gray)
io.show()