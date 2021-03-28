from enum import Enum
from random import *

from Inspector import Inspector
from Random import RandomNum
from Workstation import Workstation


class States(Enum):
    WAITING = 1
    BLOCKED = 2
    WORKING = 3

'''
Initialize classes
return tuple containing arrays of inspectors and workstations
'''
def initClasses():
    
    workS1 = Workstation(1, "C1", "", States.WAITING)
    workS2 = Workstation(2, "C1", "C2", States.WAITING)
    workS3 = Workstation(3, "C1", "C3", States.WAITING)
    
    inspector1 = Inspector(1, "C1", "", States.WAITING)     #Formerlly insp1
    inspector2 = Inspector(2, "C2", "C3", States.WAITING)   #Formerly insp2
    
    inspectors = [inspector1,inspector2]
    workstations = [workS1,workS2,workS3]
    
    return (inspectors,workstations)

'''
If inspector waiting, create new component then set working
if inspector working, do nothing
if inspector blocked, do nothing
'''
def checkInspectors(inspector,currentTime):
    if inspector.state == States.WAITING:
        inspector.inspect(currentTime)
        inspector.setState(States.WORKING)
    elif inspector.state == States.WORKING:
        if currentTime > inspector.getNextTime():
            inspector.setState(States.BLOCKED)
    # State change from blocked to waiting occurs during buffer check
    # elif inspector.state == States.BLOCKED:

'''
Check if a buffer is available to add the inspector's component
'''
def checkBufferCapacity(component, workstations):
    for i in workstations:
        if i.checkBuffer(component.name) < 2:
            return True
            
'''
If Inspector has component available
Requires buffer lengths to be checked
TODO: Log blocked time of inspector
'''
def addToBuffer(inspector,workstations,inspectorBlockedList):
    #Check buffer capacity before accepting component
    if inspector.state == States.BLOCKED:
        if checkBufferCapacity(inspector.peakComponent(),workstations):
            component = inspector.getComponent()
            #C2 or C3 directed to appropriate buffer
            if component.name != "C1":
                for i in workstations:
                    i.addComponent(component)
            #C1 optimization assuming three C1 buffers
            for i in range(2):
                addedComponent = False
                for j in workstations:
                    if j.checkbuffer(component.name) == i:
                        j.addComponent(component)
                        addedComponent = True
                        break
                if addedComponent == True:
                    break
            inspector.setState(States.WAITING)
            inspectorBlockedList.append([component.name,inspector.blockedTime])

'''
Update workstation states
if working, check for switch, return product, update product time
If waiting, do nothing
'''
def checkWorkstation(workstation, currentTime, productList):
    if workstation.state == States.WORKING:
        if currentTime > workstation.getNextTime():
            product = workstation.getProduct()
            product.calculateProductionTime(currentTime)
            productList.append(product)
            workstation.setState(States.WAITING)
            
    # if workstation.state == States.WAITING:
        
'''
If workstation waiting, assemble and produce product
TO DO: Check timing, product times
'''
def assembleWorkstations(workstations):
    for i in workstations:
        if i.getState() == States.WAITING and i.checkAssemble():
            i.assemble()
            
            
def getNextTime(inspectors,workstations,currentTime):
    nextTime = inspectors[0].getNextTime()
    for i in inspectors:
        if i.getNextTime() < nextTime:
            nextTime = i.getNextTime()
    
    for i in workstations:
        if i.getNextTime() < nextTime:
            nextTime = i.getNextTime()
    
    if nextTime < currentTime:
        print("Error: nextTime < currentTime")
    
    return nextTime

def main():
    
    inspectors,workstations = initClasses()
    
    productList = []
    inspectorBlockedList = []
    currentTime = 0
    
    while currentTime < 1000:
        #Step 1: Inspectors create component 
        for i in inspectors:
            checkInspectors(i,currentTime)
        
        #Step 2: Add component to buffer 
        for i in inspectors:
            addToBuffer(i,workstations,inspectorBlockedList)
            
        #Step 3: Recheck inspectors
        for i in inspectors:
            checkInspectors(i,currentTime)
        
        #Step 3: Update workstation states
        #TO DO: Gather products, detect assembly times
        for i in workstations:
            checkWorkstation(i, currentTime, productList)
        
        #Step 4: Assemble Products
        assembleWorkstations(workstations)
        
        currentTime = getNextTime(inspectors,workstations,currentTime)
    

if __name__ == "__main__":
    main()