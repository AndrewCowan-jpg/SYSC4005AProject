import math
from enum import Enum

import pandas as pd
from Calculations import Calculations
from Inspector import Inspector
from Workstation import Workstation

'''
Change run time to change simulation length
'''
RUN_TIME = 20000

# dataframes for the calculated values of each replica
blockTimes = pd.DataFrame(columns=['Replica', 'Total Blocked Time', 'TE'])
throughput = pd.DataFrame(columns=['Replica', 'Throughput(product/hour)', 'TE'])
initialBT = pd.DataFrame(columns=['Replica', 'Total Blocked Time', 'TE+TO'])
initialTP = pd.DataFrame(columns=['Replica', 'Throughput(product/hour)', 'TE+TO'])

# Number of sim replications
TOTAL_REPS = 10

TO = 2000

alternate = 0


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
    calculations = Calculations(TOTAL_REPS, RUN_TIME, TO)
    inspector1 = Inspector(1, "C1", "", States.WAITING)  # Formerlly insp1
    inspector2 = Inspector(2, "C2", "C3", States.WAITING)  # Formerly insp2
    inspectors = [inspector1, inspector2]
    workstations = [workS1, workS2, workS3]

    return inspectors, workstations, calculations


'''
If inspector waiting, create new component then set working
if inspector working, do nothing
if inspector blocked, do nothing
'''
def checkInspectors(inspector, currentTime):
    if inspector.state == States.WAITING:
        inspector.inspect(currentTime)
        inspector.setState(States.WORKING)
    elif inspector.state == States.WORKING:
        if currentTime >= inspector.getNextTime():
            inspector.setState(States.BLOCKED)

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
'''
def addToBuffer(inspector, workstations, currentTime, inspectorBlockedList, initialInspectorB):
    # Check buffer capacity before accepting component
    if inspector.state == States.BLOCKED:
        if checkBufferCapacity(inspector.peakComponent(), workstations):
            component = inspector.getComponent(currentTime)

            # C2 or C3 directed to appropriate buffer
            if component.name == "C2" or component.name == "C3":
                for i in workstations:
                    if i.addComponent(component):
                        break

            # C1 optimization assuming three C1 buffers
            elif component.name == "C1":
                schedulingAlternative2(workstations, component)

            inspector.setState(States.WAITING)
            if inspector.blockedTime > 0:
                if currentTime > TO:
                    inspectorBlockedList.append(
                        [component.name, inspector.blockedTime, currentTime - inspector.blockedTime])
                initialInspectorB.append([component.name, inspector.blockedTime, currentTime - inspector.blockedTime])

'''
Original Scheduling for Inspector 1
'''
def originalScheduling(workstations, component):
    for i in range(2):
        addedComponent = False
        for j in workstations:
            if j.checkBuffer(component.name) == i:
                if j.addComponent(component):
                    addedComponent = True
                    break
        if addedComponent:
            break

'''
Alternate Scheduling for Inspector 1 
'''
def schedulingAlternative1(workstations, component):
    global alternate
    if alternate == 0 and workstations[alternate].checkBuffer(component.name) < 2:
        workstations[alternate].addComponent(component)
        alternate = 1
    elif alternate == 1 and workstations[alternate].checkBuffer(component.name) < 2:
        workstations[alternate].addComponent(component)
        alternate = 2
    elif alternate == 2 and workstations[alternate].checkBuffer(component.name) < 2:
        workstations[alternate].addComponent(component)
        alternate = 0
    else:
        if alternate < 2:
            alternate += 1
            schedulingAlternative1(workstations, component)
        else:
            alternate = 0
            schedulingAlternative1(workstations, component)

'''
Alternate Scheduling for Inspector 1 
'''
def schedulingAlternative2(workstation, component):
    if workstation[1].checkBuffer("C2") > 0 and workstation[1].checkBuffer(component.name) < 2:
        workstation[1].addComponent(component)
    elif workstation[2].checkBuffer("C3") > 0 and workstation[1].checkBuffer(component.name) < 2:
        workstation[2].addComponent(component)
    elif workstation[0].checkBuffer(component.name) < 2:
        workstation[0].addComponent(component)

'''
Update workstation states
if working, check for switch, return product, update product time
If waiting, do nothing
'''
def checkWorkstation(workstation, currentTime, productList, initialProduct):
    if workstation.state == States.WORKING:
        if currentTime >= workstation.getNextTime():
            product = workstation.getProduct()
            product.calculateProductionTime(workstation.getNextTime())
            if currentTime > TO:
                productList.append([product.name, product.totalTime, currentTime])
            initialProduct.append([product.name, product.totalTime, currentTime])
            workstation.setState(States.WAITING)


'''
If workstation waiting, assemble and produce product
'''
def assembleWorkstations(workstations, currentTime):
    for i in workstations:
        if i.getState() == States.WAITING and i.checkAssemble():
            i.assemble(currentTime)
            i.setState(States.WORKING)

'''
Smallest value is current time
Second smallest is next time
'''
def getNextTime(inspectors, workstations, currentTime):
    nextTime = RUN_TIME
    for i in inspectors:
        if i.getNextTime() < nextTime and i.getNextTime() > currentTime:
            nextTime = i.getNextTime()

    for j in workstations:
        if j.getNextTime() < nextTime and j.getNextTime() > currentTime:
            nextTime = j.getNextTime()

    if nextTime < currentTime:
        print("Error: nextTime < currentTime")

    return nextTime


def main(replica):
    inspectors, workstations, calculations = initClasses()
    productList = []
    initialProduct = []
    inspectorBlockedList = []
    initialInspectorB = []
    currentTime = 0

    while currentTime < RUN_TIME:
        # This loop accounts for system changes at the same time
        for j in range(3):
            # Step 1: Inspectors create component
            for i in inspectors:
                checkInspectors(i, currentTime)

            # Step 2: Add component to buffer
            for i in inspectors:
                addToBuffer(i, workstations, currentTime, inspectorBlockedList, initialInspectorB)

            # Step 3: Recheck inspectors
            for i in inspectors:
                checkInspectors(i, currentTime)

            # Step 3: Update workstation states
            for i in workstations:
                checkWorkstation(i, currentTime, productList, initialProduct)

            # Step 4: Assemble Products
            assembleWorkstations(workstations, currentTime)

        # Step 5: Increment time
        currentTime = getNextTime(inspectors, workstations, currentTime)

    # Calculation Section
    products = pd.DataFrame(productList, columns=['Product', 'Production Time', 'Simulation Time'])
    blockedInspector = pd.DataFrame(inspectorBlockedList, columns=['Inspector', 'Blocked Time', 'Simulation Time'])
    iProducts = pd.DataFrame(initialProduct, columns=['Product', 'Production Time', 'Simulation Time'])
    iBlockedInspector = pd.DataFrame(initialInspectorB, columns=['Inspector', 'Blocked Time', 'Simulation Time'])
    calculations.outputInspector(replica, blockedInspector, False)
    calculations.outputProduct(replica, products, False)
    calculations.outputInspector(replica, iBlockedInspector, True)
    calculations.outputProduct(replica, iProducts, True)
    calculations.eachProductThroughput(replica, products)
    initialBT.loc[replica] = calculations.totalBlockedTime(replica, iBlockedInspector, True)
    initialTP.loc[replica] = calculations.productThroughput(replica, iProducts, True)
    blockTimes.loc[replica] = calculations.totalBlockedTime(replica, blockedInspector, False)
    throughput.loc[replica] = calculations.productThroughput(replica, products, False)

    if replica == TOTAL_REPS:
        calculations.throughputCalc(initialTP, True)
        calculations.blockedCalc(initialBT, True)
        calculations.throughputCalc(throughput, False)
        calculations.blockedCalc(blockTimes, False)

if __name__ == "__main__":
    for r in range(1, TOTAL_REPS + 1):
        main(r)
