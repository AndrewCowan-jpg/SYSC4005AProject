import csv
import random
import pandas as pd
import numpy as np


c1 = pd.DataFrame(columns=['Time Interval'])
c2 = pd.DataFrame(columns=['Time Interval'])
c3 = pd.DataFrame(columns=['Time Interval'])
w1 = pd.DataFrame(columns=['Time Interval'])
w2 = pd.DataFrame(columns=['Time Interval'])
w3 = pd.DataFrame(columns=['Time Interval'])

class Random():
    def __init__(self, name):
        self.name = name
        self.index = 0;
        for i in range(300):
            c1.loc[i] = (-1/0.09654457318) * np.log(random.random())
            c2.loc[i] = (-1/0.06436288999) * np.log(random.random())
            c3.loc[i] = (-1/0.04846662112) * np.log(random.random())
            w1.loc[i] = (-1/0.2171827774) * np.log(random.random())
            w2.loc[i] = (-1/0.09015013604) * np.log(random.random())
            c1.loc[i] = (-1/0.1136934688) * np.log(random.random())
        print(c1)


    def getTimeInterval(self):
        if self.name == "C1":
            if self.index < 300:
                timeInt = c1._get_value(self.index, 'Time Interval')
                self.index += 1
                return timeInt
            else:
                return 0
        elif self.name == "C2":
            if self.index < 300:
                timeInt = c2._get_value(self.index, 'Time Interval')
                self.index += 1
                return timeInt
            else:
                return 0
        elif self.name == "C3":
            if self.index < 300:
                timeInt = c3._get_value(self.index, 'Time Interval')
                self.index += 1
                return timeInt
            else:
                return 0
        elif self.name == "W1":
            if self.index < 300:
                timeInt = w1._get_value(self.index, 'Time Interval')
                self.index += 1
                return timeInt
            else:
                return 0
        elif self.name == "W2":
            if self.index < 300:
                timeInt = w2._get_value(self.index, 'Time Interval')
                self.index += 1
                return timeInt
            else:
                return 0
        elif self.name == "W3":
            if self.index < 300:
                timeInt = w3._get_value(self.index, 'Time Interval')
                self.index += 1
                return timeInt
            else:
                return 0
        else:
            return 0

