import numpy as np
import math

class SinogramGenerator:
    n = 360 # liczba detektorow
    l = 360 # kat zasiegu detektorow
    alfa = 1 # kat o jaki przesuwac co krok
    withFilter = False

    def __init__(self, img):
        self.img = img
    
    def generate(self, img):
        self.img = img
        ilosc = int(360 / self.alfa)
        self.initiateData(img, ilosc)
        self.sinogram = np.zeros((ilosc, self.n))
        self.generateKernel()
        for i in range(ilosc):
            alfa = self.alfa * i
            if i%10 == 0:
                print(alfa)
            emitter = self.createEmitter(alfa)
            detectors = self.createDetectors(alfa)
            for nr, (x, y) in enumerate(detectors):
                self.sinogram[i, nr] = self.getRayValue(emitter, (x, y))
            if self.withFilter == True:
                self.sinogram[i] = self.filter(self.sinogram[i])
        if self.withFilter == True:
            min = np.min(self.sinogram)
            self.sinogram = self.sinogram - min
            max = np.max(self.sinogram)            
            self.sinogram = self.sinogram/max
        return self.sinogram

    def revert(self):   
        ilosc = int(360 / self.alfa)
        self.reverted = np.zeros(self.img.shape)
        self.amount = np.zeros(self.img.shape)
        for i in range(ilosc):
            alfa = self.alfa * i
            emitter = self.createEmitter(alfa)
            detectors = self.createDetectors(alfa)
            for nr, (x, y) in enumerate(detectors):
                value = self.sinogram[i, nr]                        
                self.colorPixelsInPath(emitter, (x, y), value)
        for i in range(self.reverted.shape[0]):
            for j in range(self.reverted.shape[1]):
                self.reverted[i, j] = self.reverted[i, j]/ self.amount[i, j]
        return self.reverted

    def initiateData(self, img, ilosc):
        self.x_max = img.shape[0]
        self.y_max = img.shape[1]
        self.amount = np.zeros(img.shape)
        self.center = [int(self.x_max/2), int(self.y_max/2)]
        self.r = int(np.sqrt(pow(self.center[0], 2)+pow(self.center[1], 2)))
    
    def createEmitter(self, alfa):
        x = self.center[0] + self.r * np.cos(np.deg2rad(alfa))
        y = self.center[1] + self.r * np.sin(np.deg2rad(alfa))
        return [int(x), int(y)]
    
    def createDetectors(self, alfa):
        detectors = []
        for i in range(self.n):
            arg = np.deg2rad(alfa) + np.pi - np.deg2rad(self.l)/2 + i * (np.deg2rad(self.l)/(self.n - 1))
            x = self.center[0] + self.r * np.cos(arg)
            y = self.center[1] + self.r * np.sin(arg)
            detectors.append([int(x), int(y)])
        return detectors
    
    def getRayValue(self, emitter, detector):
        x1, y1 = emitter
        x2, y2 = detector
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
        value = 0
        count = 0
        for i in range(int(x1), int(x2 + 1)):
            if obrot:
                val, cnt = self.getValue(y1, i)
                value += val
                count += cnt
            else:
                val, cnt = self.getValue(i, y1)
                value += val
                count += cnt
            e -= abs(dy)
            if e < 0:
                y1 += krok
                e +=dx
        if count != 0:
            return value/count
        else:
            return value

    def colorPixelsInPath(self, emitter, detector, value):
        x1, y1 = emitter
        x2, y2 = detector
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
        for i in range(int(x1), int(x2 + 1)):
            if obrot:
                if y1 >= 0 and y1 < self.x_max and i >=0 and i < self.y_max:
                    self.amount[y1, i] += 1
                    self.reverted[y1, i] += value
            else:
                if y1 >= 0 and y1 < self.y_max and i >=0 and i < self.x_max:
                    self.reverted[i, y1] += value
                    self.amount[i, y1] += 1
            e -= abs(dy)
            if e < 0:
                y1 += krok
                e +=dx

    def getValue(self, x, y):
        if x >= 0 and x < self.img.shape[0] and y >=0 and y < self.img.shape[1]:
            return self.img[x, y], 1
        else:
            return 0, 0

    def filter(self, k):
        # self.kernel = [-2, 5, -2]
        center = int(len(self.kernel)/ 2)
        # self.kernel = np.reshape(self.kernel, (self.n,))
        result = np.zeros(k.shape)
        for i in range(self.n):
            sum = 0
            count = 0
            for j in range(len(self.kernel)):
                x = i - center + j
                if x >=0 and x < self.n:
                    sum += (k[x] * self.kernel[j])
                    count += 1
            result[i] = sum
        return result

    def generateKernel(self):
        self.kernel = np.zeros(self.sinogram.shape[1])
        center = math.ceil(len(self.kernel)/ 2)
        for i in range(len(self.kernel)):
            if i == center:
                self.kernel[i] = 1
            elif i%2 == 0:
                self.kernel[i] = 0
            else:
                self.kernel[i] = (-4/np.pi**2)/((i-center)**2)