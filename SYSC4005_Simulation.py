# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 19:14:44 2021

"""

import numpy as np
import pandas as pd

FILENAME_P1 = "servinsp1.dat"
FILENAME_P2 = "servinsp2.dat"
FILENAME_P3 = "servinsp3.dat"

FILENAME_W1 = "ws1.dat"
FILENAME_W2 = "ws2.dat"
FILENAME_W3 = "ws3.dat"


class Inspector:
    '''
    inspectorStatus:
        0 = blocked
        1 = working
    currentComponent:
        0 = C1
        1 = C2
        2 = C3
    '''
    def __init__(self, inspectorID):
        self.inspectorID = inspectorID
        self.inspectorStatus = 0;
        self.currentComponent = 0;
        
        
def main():
    dat = pd.read_csv(FILENAME_W1).to_numpy()
    # dat = dat.to_numpy()
    # for i in dat:
    #     print(i)
    print(dat)

if __name__ == "__main__":
    main()
