from Component import Component
from Random import RandomNum
from random import *

order = 0
        
class Inspector():
    def __init__(self, num, componentT1, componentT2, state):
        self.inspectorNum = num       #Ex. "1 or 2"
        self.componentT1 = componentT1       #Ex "C1" or "C2"
        self.componentT2 = componentT2       #Ex "C3" or null
        self.state = state
        
        self.component = None #Stores component created during inspection
        
        self.currentTime = 0     #Used to calculated blocked time
        self.blockedTime = 0    #Time spent blocked
        self.inspectionTime = 0  #Time to inspect component
        self.nextTime = 0       #Contains the time for switching from WAITING to WORKING
        
        self.componentDict = {
            self.componentT1: RandomNum(self.componentT1),
            self.componentT2: RandomNum(self.componentT2)     #inspector1 uses null for T2
        }

    '''
    Create component based on C1, C2 or C3
    saves component object with current time where inpsection started
    Updates the inspection time
    '''
    def inspect(self, currentTime):

        self.currentTime = currentTime     #possible removal, may not be required
        if self.componentT1 == "C1":
            self.inspectionTime = self.componentDict[self.componentT1].getRand()
            self.component = Component(self.componentT1, self.currentTime)
        else:
            self.alternateSelection()
        
        self.getNextTime()

    def originalSelection(self):
        randomNumber = randrange(2)  # Creates number between 0 and 1
        if randomNumber == 1:
            self.inspectionTime = self.componentDict[self.componentT1].getRand()
            self.component = Component(self.componentT1, self.currentTime)
        else:
            self.inspectionTime = self.componentDict[self.componentT2].getRand()
            self.component = Component(self.componentT2, self.currentTime)

    def alternateSelection(self):
        global order
        if order == 0:
            self.inspectionTime = self.componentDict[self.componentT1].getRand()
            self.component = Component(self.componentT1, self.currentTime)
            order += 1
        else:
            self.inspectionTime = self.componentDict[self.componentT2].getRand()
            self.component = Component(self.componentT2, self.currentTime)
            order = 0

    def getNextTime(self):
        self.nextTime = self.currentTime + self.inspectionTime
        # print("Inspector Next Time = " + str(self.nextTime))
        return self.nextTime
    
    def setState(self, state):
        self.state = state

    def peakComponent(self):
        return self.component
    
    '''
    Removes components from inspector and updates time blocked
    '''
    def getComponent(self, currentTime):
        self.blockedTime = currentTime - self.nextTime
        
        tempComponent = self.component
        self.component = None
        return tempComponent