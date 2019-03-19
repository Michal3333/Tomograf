
def getPoints((x1, y1), (x2, y2)):
    dx = abs(x1-x2)
    dy = abs(y1 -y2)
    if x1 <= x2:
        kx = 1
    else:
        kx = -1

    if y1 <= y2:
        ky = 1
    else:
        ky = -1
    e = 0;
    if dy > dx:
        #interate over y
        e = dy / 2
        for i in range(dy):
            
    else:
        #interate over x
        e = dx / 2



getPoints()