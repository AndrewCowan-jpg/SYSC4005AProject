from Milestone3.Component import Component
import random as rand


class Inspector():
    def __init__(self, num, componentT1, componentT2, state):
        self.inspectorNum = num
        self.componentT1 = componentT1
        self.componentT2 = componentT2
        self.state = state
        self.blockTime = 0
        self.blockC = ""

    def inspect(self, startT, component):
        if self.inspectorNum == 1:
            return Component("C1", startT)
        else:
            if component == "C2":
                return Component("C2", startT)
            else:
                return Component("C3", startT)

    def setState(self, state):
        self.state = state

    def timeBlocked(self, timeBlocked):
        self.blockTime += timeBlocked

    def componentBlocked(self, component):
        self.blockC = component