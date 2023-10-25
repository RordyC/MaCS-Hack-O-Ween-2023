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

def lineRect(x1,y1,x2,y2,rx,ry,rw,rh,edges):
    top, bottom, left, right = edges

    if edges[0]: top = lineLine(x1, y1, x2, y2, rx, ry, rx + rw, ry)
    if edges[1]: bottom = lineLine(x1, y1, x2, y2, rx, ry + rh, rx + rw, ry + rh)
    if edges[2]: left = lineLine(x1, y1, x2, y2, rx, ry, rx, ry + rh)
    if edges[3]: right = lineLine(x1, y1, x2, y2, rx + rw, ry, rx + rw, ry + rh)

    return left or right or top or bottom
def lineLine(x1,y1,x2,y2,x3,y3,x4,y4):
    uA = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))
    uB = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))

    if (uA >= 0 and uA <= 1 and uB >= 0 and uB <= 1):
        intX = x1 + (uA * (x2-x1))
        intY = y1 + (uA * (y2-y1))
        return True

    else: return False

def circleRectMove(cx, potentialPosition,tileX,tileY):
    nearestPoint = [0,0]
    nearestPoint[0] = max(float(tileX), min(potentialPosition[0], float(tileX+32)))
    nearestPoint[1] = max(float(tileY), min(potentialPosition[1], float(tileY+32)))
    rayToNearest = [0,0]
    rayToNearest[0] = nearestPoint[0] - potentialPosition[0]
    rayToNearest[1] = nearestPoint[1] - potentialPosition[1]

    rayMag = sqrt((rayToNearest[0]*rayToNearest[0])+(rayToNearest[1]*rayToNearest[1]))
    overlap = cx - rayMag
    if (overlap > 0):

        potentialPosition[0] = potentialPosition[0] - (rayToNearest[0]/rayMag) * overlap
        potentialPosition[1] = potentialPosition[1] - (rayToNearest[1]/rayMag) * overlap

    return potentialPosition

def pointCircle(pointX, pointY, circleX, circleY, r):
  distX = pointX - circleX
  distY = pointY - circleY
  distanceSqrd = (distX*distX) + (distY*distY)

  return (distanceSqrd <= (r*r))


