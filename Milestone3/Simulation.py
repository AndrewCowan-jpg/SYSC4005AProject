from enum import Enum
import csv
import numpy as np
import pandas as pd


# with open('RandomTimes/W1.csv', newline='') as csvfile:
#     W1 = list(csv.reader(csvfile))
# with open('RandomTimes/W2.csv', newline='') as csvfile:
#     W2 = list(csv.reader(csvfile))
# with open('RandomTimes/W3.csv', newline='') as csvfile:
#     W3 = list(csv.reader(csvfile))
# with open('RandomTimes/C1.csv', newline='') as csvfile:
#     C1 = list(csv.reader(csvfile))
# with open('RandomTimes/C2.csv', newline='') as csvfile:
#     C2 = list(csv.reader(csvfile))
# with open('RandomTimes/C3.csv', newline='') as csvfile:
#     C3 = list(csv.reader(csvfile))

def sortList(dictionary,timeList, datFile):
    for i in range(len(timeList)):
        inserted = 0
        for j in range(len(dictionary)):
            if timeList[i] < dictionary[j][0]:
                dictionary.insert(j,[timeList[i],datFile])
                inserted = 1
                break
        if inserted == 0:
            dictionary.insert(len(dictionary),[timeList[i],datFile])
            
    
def initDict(eventList,timeList, datFile):
    for i in range(len(timeList)):
        eventList.insert(i,[timeList[i],datFile])
    

def main():
    FILENAME_P1 = "servinsp1.dat"
    FILENAME_P2 = "servinsp22.dat"
    FILENAME_P3 = "servinsp23.dat"
    
    FILENAME_W1 = "ws1.dat"
    FILENAME_W2 = "ws2.dat"
    FILENAME_W3 = "ws3.dat"
    
    FOLDER_PATH = "C:\\Users\\DREW\\Desktop\\SYSC4005\\SYSC4005AProject\\"
    
    
    w1 = pd.read_csv(FOLDER_PATH + FILENAME_W1, header=None).to_numpy()
    w2 = pd.read_csv(FOLDER_PATH + FILENAME_W2, header=None).to_numpy()
    w3 = pd.read_csv(FOLDER_PATH + FILENAME_W3, header=None).to_numpy()
    
    c1 = pd.read_csv(FOLDER_PATH + FILENAME_P1, header=None).to_numpy()
    c2 = pd.read_csv(FOLDER_PATH + FILENAME_P2, header=None).to_numpy()
    c3 = pd.read_csv(FOLDER_PATH + FILENAME_P3, header=None).to_numpy()
    
    eventList = []
      
    print("W1:" + str(len(w1)))
    print("W2:" + str(len(w2)))
    print("W3:" + str(len(w3)))
    print("C1:" + str(len(c1)))
    print("C2:" + str(len(c2)))
    print("C3:" + str(len(c3)))  

    w1.sort(axis=0)
    w2.sort(axis=0)
    w3.sort(axis=0)
    
    c1.sort(axis=0)
    c2.sort(axis=0)
    c3.sort(axis=0)
    
    initDict(eventList,w1,"W1")
    # sortList(eventList,w1,"W1")
    sortList(eventList,w2,"W2")
    sortList(eventList,w2,"W3")
    
    sortList(eventList,c1,"C1")
    sortList(eventList,c2,"C2")
    sortList(eventList,c3,"C3")
    
    count = 0
    for i in eventList:
        print(str(i[0]) + " " + i[1])
        # count = count + 1
        # if count > 50:
        #     break
        
    print(len(eventList))


if __name__ == "__main__":
    main()


