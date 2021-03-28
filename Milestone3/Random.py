import random
import numpy as np

class RandomNum():
    def __init__(self, name):
        self.name = name
        self.type = {}
        self.type['C1'] = 0.09654457318
        self.type['C2'] = 0.06436288999
        self.type['C3'] = 0.04846662112
        self.type['W1'] = 0.2171827774
        self.type['W2'] = 0.09015013604
        self.type['W3'] = 0.1136934688

    def getRand(self):
        lam = self.type[self.name]
        return (-1/lam) * np.log(random.random())