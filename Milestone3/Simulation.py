from enum import Enum
import csv

with open('RandomTimes/W1.csv', newline='') as csvfile:
    W1 = list(csv.reader(csvfile))
with open('RandomTimes/W2.csv', newline='') as csvfile:
    W2 = list(csv.reader(csvfile))
with open('RandomTimes/W3.csv', newline='') as csvfile:
    W3 = list(csv.reader(csvfile))
with open('RandomTimes/C1.csv', newline='') as csvfile:
    C1 = list(csv.reader(csvfile))
with open('RandomTimes/C2.csv', newline='') as csvfile:
    C2 = list(csv.reader(csvfile))
with open('RandomTimes/C3.csv', newline='') as csvfile:
    C3 = list(csv.reader(csvfile))

class States(Enum):
    WAITING = 0
    ASSEMBLING = 1
    BLOCKED = 2

