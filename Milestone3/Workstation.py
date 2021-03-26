from Milestone3.Product import Product

class Workstation():

    def __init__(self, num, buffer1T, buffer2T, state):
        self.workSNumber = num
        self.buffer1 = []
        self.buffer2 = []
        self.buffer1T = buffer1T
        self.buffer2T = buffer2T
        self.waitTime = 0
        self.state = state

    def addComponent(self, component):
        if component.name == self.buffer1T:
            if len(self.buffer1) <= 2:
                self.buffer1.append(component)
                return True
            else:
                return False
        elif component.name == self.buffer2T:
            if len(self.buffer2) <= 2:
                self.buffer2.append(component)
                return True
            else:
                return False

    def checkBuffer(self, bufferT):
        if bufferT == self.buffer1T:
            return len(self.buffer1)
        elif bufferT == self.buffer2T:
            return len(self.buffer2)

    def checkAssemble(self):
        if self.workSNumber == 1 and len(self.buffer1) > 0:
            return True
        elif len(self.buffer1) > 0 and len(self.buffer2) > 0:
            return True
        else:
            return False

    def assemble(self, processingT):
        if self.workSNumber == 1 and len(self.buffer1) > 0:
            self.buffer1.pop(0)
            totalTime = processingT + self.waitTime
            self.waitTime = 0
            return Product("P1", totalTime)
        elif self.workSNumber == 2 and len(self.buffer1) > 0 and len(self.buffer2) > 0:
            self.buffer1.pop(0)
            self.buffer2.pop(0)
            totalTime = processingT + self.waitTime
            self.waitTime = 0
            return Product("P2", totalTime)
        elif self.workSNumber == 3 and len(self.buffer1) > 0 and len(self.buffer2) > 0:
            self.buffer1.pop(0)
            self.buffer2.pop(0)
            totalTime = processingT + self.waitTime
            self.waitTime = 0
            return Product("P3",totalTime)

    def timeWaited(self, waitTime):
        self.waitTime += waitTime

    def setState(self, state):
        self.state = state

    def getState(self):
        return self.state.name


