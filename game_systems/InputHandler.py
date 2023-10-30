class InputHandler(object):
    def __init__(self):
        self.__mouseX = 0
        self.__mouseY = 0

        self.__lmb = False
        self.__rmb = False

        self.__currentKey = ""
        self.__wKey = False
        self.__sKey = False
        self.__aKey = False
        self.__dKey = False

        self.__upKey = False
        self.__downKey = False
        self.__leftKey = False
        self.__rightKey = False

        self.__vKey = False
        self.__equalKey = False

        self.numberKeyFunc = None
        self.keyPressedFunc = None
        self.rmbPressedFunc = None

    def lmbReleased(self):
        self.__lmb = False

    def lmbPressed(self):
        self.__lmb = True
    def rmbReleased(self):
        self.__rmb = False

    def rmbPressed(self):
        self.rmbPressedFunc()
        self.__rmb = True

    def keyPressed(self, evnt):
        evnt = evnt.lower()
        if (evnt != self.__currentKey):
            self.__currentKey = evnt
            #print("pressed: " + self.__currentKey)
            self.keyPressedFunc(evnt)
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
            if (evnt == '='):
                self.__equalKey = True
            if (evnt == 'b'):
                self.__bKey = True

            if (evnt == 'up'):
                self.__upKey = True
            if (evnt == 'down'):
                self.__downKey = True
            if (evnt == 'left'):
                self.__leftKey = True
            if (evnt == 'right'):
                self.__rightKey = True

    def keyReleased(self, evnt):
        evnt = evnt.lower()
        if (evnt == self.__currentKey):
            #print("released: " + evnt)
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
        if (evnt == '='):
            self.__equalKey = False
        if (evnt == 'b'):
            self.__bKey = False

        if (evnt == 'up'):
            self.__upKey = False
        if (evnt == 'down'):
            self.__downKey = False
        if (evnt == 'left'):
            self.__leftKey = False
        if (evnt == 'right'):
            self.__rightKey = False

        if (evnt in "1234567890"):
            self.numberKeyFunc(evnt)
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

    def getArrowYAxis(self) -> int:
        if (self.__upKey and self.__downKey):
            return 0
        elif (self.__upKey):
            return -1
        elif (self.__downKey):
            return 1
        else:
            return 0
    def getArrowXAxis(self) -> int:
        if (self.__leftKey and self.__rightKey):
            return 0
        elif (self.__rightKey):
            return 1
        elif (self.__leftKey):
            return -1
        else:
            return 0

    def getMousePressed(self) -> bool:
        return self.__lmb
    def getRMB(self) -> bool:
        return self.__rmb
    def onMotion(self,evnt):
        self.__mouseX = evnt.x
        self.__mouseY = evnt.y

    def getMousePos(self) -> tuple:
        return (self.__mouseX,self.__mouseY)
    def setNumberKeyFunc(self,func):
        self.numberKeyFunc = func
    def setKeyPressedFunc(self,func):
        self.keyPressedFunc = func
    def setRMBPressedFunc(self,func):
        self.rmbPressedFunc = func