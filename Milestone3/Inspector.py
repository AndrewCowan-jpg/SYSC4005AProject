from Milestone3.Component import Component
from Milestone3.Random import Random
from random import *


# class Inspector():
#     def __init__(self, num, componentT1, componentT2, state):
#         self.inspectorNum = num
#         self.componentT1 = componentT1
#         self.componentT2 = componentT2
#         self.state = state
#         self.blockTime = 0
#         self.blockC = ""

#     def inspect(self, startT, component):
#         if self.inspectorNum == 1:
#             return Component("C1", startT)
#         else:
#             if component == "C2":
#                 return Component("C2", startT)
#             else:
#                 return Component("C3", startT)

#     def setState(self, state):
#         self.state = state

#     def timeBlocked(self, timeBlocked):
#         self.blockTime += timeBlocked

#     def componentBlocked(self, component):
#         self.blockC = component
        
        
        
class Inspector():
    def __init__(self, num, componentT1, componentT2, state):
        self.inspectorNum = num       #Ex. "1 or 2"
        self.componentT1 = componentT1       #Ex "C1" or "C2"
        self.componentT2 = componentT2       #Ex "C3" or null
        self.state = state
        
        self.component = None #Stores component created during inspection
        
        self.currentTime = 0     #Used to calculated blocked time
        self.inspectionTime = 0
        self.blockTime = 0
        self.componentDict = {
            self.componentT1 : Random(self.componentT1),
            self.componentT2 : Random(self.componentT2)     #inspector1 uses null for T2
        }

    '''
    Create component based on C1, C2 or C3
    saves component object with current time where inpsection started
    Updates the inspection time
    '''
    def inspect(self, currentTime):
        self.currentTime = currentTime     #possible removal, may not be required
        if self.componentT1 == "C1":
            self.inspectionTime = componentDict[self.componentT1].getRand()
            self.component = Component(self.componentT1,self.currentTime)
        else:
            randomNumber = randrange(2) #Creates number between 0 and 1
            if randomNumber == 1:
                self.inspectionTime = componentDict[self.componentT1].getRand()
                self.component = Component(self.componentT1,self.currentTime)
            else:
                self.inspectionTime = componentDict[self.componentT2].getRand()
                self.component = Component(self.componentT2,self.currentTime)
        

    def setState(self, state):
        self.state = state

    '''
    Calculate blocked time using current time if blocked vs time of last component created
    '''
    def timeBlocked(self, timeBlocked):
        self.blockTime = timeBlocked - self.currentTime

