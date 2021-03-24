from enum import Enum

import self as self

from Milestone3.Product import Product


class States(Enum):
    WAITING = 0
    ASSEMBLING = 1


class Workstation1():

    def __init__(self):
        self.buffer = []

    def addComponent(self, component):
        if len(self.buffer) <= 2:
            self.buffer.append(component)
            return True
        else:
            return False

    def checkBuffer(self):
        if len(self.buffer) <= 2:
            return True
        else:
            return False

    def assemble(self):
        if len(self.buffer) > 0:
            self.buffer.pop(0)
            return Product("P1")
