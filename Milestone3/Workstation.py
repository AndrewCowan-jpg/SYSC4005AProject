from Product import Product
from Random import RandomNum

class Workstation():

    def __init__(self, num, buffer1T, buffer2T, state):
        self.workSNumber = num
        self.buffer1 = []
        self.buffer2 = []
        self.buffer1T = buffer1T
        self.buffer2T = buffer2T

        self.state = state
        
        self.random = RandomNum("W"+str(num))
        
        self.currentTime = 0     #Used to calculated blocked time
        self.inspectionTime = 0  #Time to inspect component
        self.nextTime = 0       #Contains the time for switching from WAITING to WORKING
        
        self.product = None

    '''
    Workstation contains buffers
    Size check occurs outside workstation object
    '''
    def addComponent(self, component):
        if component.name == self.buffer1T:
            if len(self.buffer1) <= 2:
                self.buffer1.append(component)
                return True
        elif component.name == self.buffer2T:
            if len(self.buffer2) <= 2:
                self.buffer2.append(component)
                return True
        else:
            return False
                
    '''
    Used for size check of buffers
    '''
    def checkBuffer(self, bufferT):
        if bufferT == self.buffer1T:
            return len(self.buffer1)
        elif bufferT == self.buffer2T:
            return len(self.buffer2)
        else:
            return 2
    
    '''
    Used for workstation to determine if components available to assemble
    '''
    def checkAssemble(self):
        if self.workSNumber == 1 and len(self.buffer1) > 0:
            return True
        elif len(self.buffer1) > 0 and len(self.buffer2) > 0:
            return True
        else:
            return False

    '''
    Begins assembly process
    '''
    def assemble(self, currentTime):
        self.currentTime = currentTime
        if self.workSNumber == 1 and len(self.buffer1) > 0:
            component1 = self.buffer1.pop(0)
            self.product = Product("P1", component1, None)

        elif self.workSNumber == 2 and len(self.buffer1) > 0 and len(self.buffer2) > 0:
            component1 = self.buffer1.pop(0)
            component2 = self.buffer2.pop(0)
            self.product = Product("P2", component1, component2)

        elif self.workSNumber == 3 and len(self.buffer1) > 0 and len(self.buffer2) > 0:
            component1 = self.buffer1.pop(0)
            component2 = self.buffer2.pop(0)
            self.product = Product("P3", component1, component2)
        
        self.inspectionTime = self.random.getRand()
        self.getNextTime()
    
    '''
    Updates time action time
    '''
    def getNextTime(self):
        self.nextTime = self.currentTime + self.inspectionTime
        # print("Workstation Next Time = " + str(self.nextTime))
        return self.nextTime
    
    def getProduct(self):
        tempProduct = self.product
        self.product = None
        return tempProduct

    def setState(self, state):
        self.state = state

    def getState(self):
        return self.state

    '''
    Used for buffer optimization, check if waiting for C1 component
    
    Assumes:
        C1 buffer is empty
    
    Output:
        True if waiting for C1
    '''
    def checkWaitingC1(self):
        #WS1 check if buffer 1 empty
        if self.workSNumber == 1:
            return True
        
        #WS2/3 check if buffer 1 empty and buffer 2 not empty
        elif self.workSNumber == 2:
            if len(self.buffer2) > 0:
                return True
        
        elif self.workSNumber == 2:
            if len(self.buffer2) > 0:
                return True
        
        return False
            