import numpy as np

class SinogramGenerator:
    n = 201 # liczba detektorow
    l = 360 # kat zasiegu detektorow
    alfa = 0.5 # kat o jaki przesuwac co krok

    def __init__(self, img):
        self.img = img
    
    def generate(self, img):
        self.img = img
        self.initiateData(img)
        ilosc = int(360 / self.alfa)
        self.sinogram = np.zeros((self.n, ilosc))

        for i in range(ilosc):
            alfa = self.alfa * i
            emitter = self.createEmitter(alfa)
            detectors = self.createDetectors(alfa)
            for nr, (x, y) in enumerate(detectors):
                self.sinogram[nr, i] = self.getRayValue(emitter, (x, y))
        self.sinogram = self.sinogram
        
        return self.sinogram

    def revert(self):
        ilosc = int(360 / self.alfa)
        self.reverted = np.zeros(self.img.shape)
        
        for i in range(ilosc):
            alfa = self.alfa * i
            emitter = self.createEmitter(alfa)
            detectors = self.createDetectors(alfa)
            for nr, (x, y) in enumerate(detectors):
                value = self.getSinogramValue(nr, i)                        
                self.colorPixelsInPath(emitter, (x, y), value)
        for i in range(self.reverted.shape[0]):
            for j in range(self.reverted.shape[1]):
                self.reverted[i, j] = self.reverted[i, j]/ self.amount[i, j]
        return self.reverted

    def initiateData(self, img):
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
                    self.reverted[y1, i] += value
            else:
                if y1 >= 0 and y1 < self.y_max and i >=0 and i < self.x_max:
                    self.reverted[i, y1] += value
            e -= abs(dy)
            if e < 0:
                y1 += krok
                e +=dx

    def getValue(self, x, y):
        if x >= 0 and x < self.x_max and y >=0 and y < self.y_max:
            self.amount[x, y] += 1
            return self.img[x, y], 1
        else:
            return 0, 0
    
    def getSinogramValue(self, x, y):
        if x >= 0 and x < self.x_max and y >=0 and y < self.y_max:
            return self.sinogram[x, y]
        else:
            return 0