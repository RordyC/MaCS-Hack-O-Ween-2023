from math import sqrt
# 
def circleRect(cx,cy,r,rx,ry,rw,rh):
    testX = cx
    testY = cy

    if (cx < rx): testX = rx
    elif (cx > (rx +rw)): testX = rx+rw

    if (cy < ry): testY = ry
    elif (cy>(ry+rh)): testY = ry + rh

    distX = cx-testX
    distY = cy-testY
    distance = sqrt((distX*distX) + (distY*distY))

    return (distance <= r)