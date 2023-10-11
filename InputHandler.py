class InputHandler(object):
    def __init__(self):
        self.__mouseX = 0
        self.__mouseY = 0

        self.__lmb = False

        self.__currentKey = ""
        self.__wKey = False
        self.__sKey = False
        self.__aKey = False
        self.__dKey = False

        self.__vKey = False

    def lmbReleased(self):
        self.__lmb = False

    def lmbPressed(self):
        self.__lmb = True

    def keyPressed(self, evnt):
        evnt = evnt.lower()
        if (evnt != self.__currentKey):
            self.__currentKey = evnt
            print("pressed: " + self.__currentKey)
            if (evnt == "w"):
                self.__wKey = True
            if (evnt == "s"):
                self.__sKey = True
            if (evnt == "a"):
                self.__aKey = True
            if (evnt == "d"):
                self.__dKey = True
            if (evnt == 'v'):
                self.__vKey = True

    def keyReleased(self, evnt):
        evnt = evnt.lower()
        if (evnt == self.__currentKey):
            print("released: " + evnt)
            self.__currentKey = ""

        if (evnt == "w"):
            self.__wKey = False
        if (evnt == "s"):
            self.__sKey = False
        if (evnt == "a"):
            self.__aKey = False
        if (evnt == "d"):
            self.__dKey = False
        if (evnt == 'v'):
            self.__vKey = False

    def getYAxis(self) -> int:
        if (self.__wKey and self.__sKey):
            return 0
        elif (self.__wKey):
            return -1
        elif (self.__sKey):
            return 1
        else:
            return 0
    def getXAxis(self) -> int:
        if (self.__aKey and self.__dKey):
            return 0
        elif (self.__dKey):
            return 1
        elif (self.__aKey):
            return -1
        else:
            return 0

    def getMousePressed(self) -> bool:
        return self.__lmb
    def onMotion(self,evnt):
        self.__mouseX = evnt.x
        self.__mouseY = evnt.y

    def getMousePos(self) -> tuple:
        return (self.__mouseX,self.__mouseY)