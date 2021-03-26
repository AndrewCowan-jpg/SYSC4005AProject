from enum import Enum
import csv
import numpy as np
import pandas as pd
import random as rand

from Milestone3.Inspector import Inspector
from Milestone3.Random import Random
from Milestone3.Workstation import Workstation


class States(Enum):
    WAITING = 1
    BLOCKED = 2
    ASSEMBLING = 3



def simulator():
    c1Times = Random("C1")
    c2Times = Random("C2")
    c3Times = Random("C3")
    w1Times = Random("W1")
    w2Times = Random("W2")
    w3Times = Random("W3")

    workStation1 = Workstation(1, "C1", "", States.WAITING)
    workStation2 = Workstation(2, "C1", "C2", States.WAITING)
    workStation3 = Workstation(3, "C2", "C3", States.WAITING)

    inspector1 = Inspector(1, "C1", "", States.WAITING)
    inspector2 = Inspector(2, "C2", "C3", States.WAITING)

    while(1):
        if inspector1.getState() == States.WAITING.name:
            inspectTime1 = c1Times.getTimeInterval()
            c1 = inspector1.inspect(inspectTime1, "C1")
        if inspector2.getState() == States.WAITING.name:
            randC = rand(2)
            if randC == 0:
                inspectTime2 = c2Times.getTimeInterval()
                c2 = inspector2.inspect(inspectTime2)
            elif randC == 1:
                inspectTime2 = c3Times.getTimeInterval()
                c3 = inspector2.inspect(inspectTime2)




