from enum import Enum
from Inspector import Inspector
from Workstation import Workstation
import pandas as pd
import math


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

    inspector1 = Inspector(1, "C1", "", States.WAITING)  # Formerlly insp1
    inspector2 = Inspector(2, "C2", "C3", States.WAITING)  # Formerly insp2

    inspectors = [inspector1, inspector2]
    workstations = [workS1, workS2, workS3]

    return inspectors, workstations


'''
If inspector waiting, create new component then set working
if inspector working, do nothing
if inspector blocked, do nothing
'''
def checkInspectors(inspector, currentTime):
    if inspector.state == States.WAITING:
        inspector.inspect(currentTime)
        inspector.setState(States.WORKING)
        # print("Inspector " + str(inspector.inspectorNum) + " WAITING TO WORKING")
        # print("Inspector " + str(inspector.inspectorNum) + " Next Time " + str(inspector.nextTime))
    elif inspector.state == States.WORKING:
        if currentTime >= inspector.getNextTime():
            inspector.setState(States.BLOCKED)
        # print("Inspector " + str(inspector.inspectorNum) + " BLOCKED")
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
'''
def addToBuffer(inspector, workstations, currentTime, inspectorBlockedList, initialInspectorB):
    # Check buffer capacity before accepting component
    if inspector.state == States.BLOCKED:
        if checkBufferCapacity(inspector.peakComponent(), workstations):
            component = inspector.getComponent(currentTime)
            # print("Component: " + component.name)

            # C2 or C3 directed to appropriate buffer
            if component.name == "C2" or component.name == "C3":
                for i in workstations:
                    if i.addComponent(component):
                        # print("Inspector " + str(
                        # inspector.inspectorNum) + " Component: " + component.name + " Added to Buffer " + str(
                        # i.workSNumber))
                        break

            # C1 optimization assuming three C1 buffers
            elif component.name == "C1":
                for i in range(2):
                    addedComponent = False
                    for j in workstations:
                        if j.checkBuffer(component.name) == i:
                            if j.addComponent(component):
                                addedComponent = True
                                # print("Inspector " + str(
                                # inspector.inspectorNum) + " Component: " + component.name + " Added to Buffer " + str(
                                # j.workSNumber))
                                break
                    if addedComponent:
                        break

            inspector.setState(States.WAITING)

            if inspector.blockedTime > 0:
                if currentTime > TO:
                    inspectorBlockedList.append([component.name, inspector.blockedTime, currentTime-inspector.blockedTime])
                initialInspectorB.append([component.name, inspector.blockedTime, currentTime-inspector.blockedTime])


'''
Update workstation states
if working, check for switch, return product, update product time
If waiting, do nothing
'''
def checkWorkstation(workstation, currentTime, productList, initialProduct):
    if workstation.state == States.WORKING:
        if currentTime >= workstation.getNextTime():
            product = workstation.getProduct()
            # print("Workstation " + str(workstation.workSNumber) + " Created Product " + product.name)
            product.calculateProductionTime(workstation.getNextTime())
            if currentTime > TO:
                productList.append([product.name, product.totalTime, currentTime])
            initialProduct.append([product.name, product.totalTime, currentTime])
            workstation.setState(States.WAITING)

    # if workstation.state == States.WAITING:


'''
If workstation waiting, assemble and produce product
'''
def assembleWorkstations(workstations, currentTime):
    for i in workstations:
        if i.getState() == States.WAITING and i.checkAssemble():
            i.assemble(currentTime)
            i.setState(States.WORKING)
            # print("Workstation " + str(i.workSNumber) + " Assembling")
            # print("Workstation " + str(i.workSNumber) + " Next Time " + str(i.nextTime))


'''
outputs the products onto a excel file 
where each sheet is a separate simulation
'''
def outputInspector(rep, dataframe, initial):
    sheetName = 'Simulation_' + str(rep)
    if initial:
        if rep > 1:
            with pd.ExcelWriter('InitialBlockedInspectors.xlsx', mode='a') as writer:
                dataframe.to_excel(writer, sheet_name=sheetName)
        else:
            with pd.ExcelWriter('InitialBlockedInspectors.xlsx') as writer:
                dataframe.to_excel(writer, sheet_name=sheetName)
    else:
        if rep > 1:
            with pd.ExcelWriter('BlockedInspectors.xlsx', mode='a') as writer:
                dataframe.to_excel(writer, sheet_name=sheetName)
        else:
            with pd.ExcelWriter('BlockedInspectors.xlsx') as writer:
                dataframe.to_excel(writer, sheet_name=sheetName)



'''
outputs the products onto a excel file 
where each sheet is a separate simulation
'''
def outputProduct(rep, dataframe, initial):
    sheetName = 'Simulation_' + str(rep)
    if initial:
        if rep > 1:
            with pd.ExcelWriter('initialProductOutputs.xlsx', mode='a') as writer:
                dataframe.to_excel(writer, sheet_name=sheetName)
        else:
            with pd.ExcelWriter('initialProductOutputs.xlsx') as writer:
                dataframe.to_excel(writer, sheet_name=sheetName)
    else:
        if rep > 1:
            with pd.ExcelWriter('productOutputs.xlsx', mode='a') as writer:
                dataframe.to_excel(writer, sheet_name=sheetName)
        else:
            with pd.ExcelWriter('productOutputs.xlsx') as writer:
                dataframe.to_excel(writer, sheet_name=sheetName)



'''
Calculates product throughput per/hour 
'''
def productThroughput(rep, dataframe, initial):
    if initial:
        return rep, len(dataframe.index) / (RUN_TIME / 60), RUN_TIME
    else:
        return rep, len(dataframe.index) / ((RUN_TIME - TO) / 60), RUN_TIME - TO


'''
Calculates the Total blocked time for each replica
'''
def totalBlockedTime(rep, dataframe, initial):
    if initial:
        return rep, dataframe['Blocked Time'].sum(), RUN_TIME
    else:
        return rep, dataframe['Blocked Time'].sum(), RUN_TIME - TO


'''
Smallest value is current time
Second smallest is next time
'''
def getNextTime(inspectors, workstations, currentTime):
    nextTime = RUN_TIME
    lastTime = RUN_TIME
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
    inspectors, workstations = initClasses()

    productList = []
    initialProduct = []
    inspectorBlockedList = []
    initialInspectorB = []
    currentTime = 0

    while currentTime < RUN_TIME:
        # print("Current Time: " + str(currentTime))

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

    products = pd.DataFrame(productList, columns=['Product', 'Production Time', 'Simulation Time'])
    blockedInspector = pd.DataFrame(inspectorBlockedList, columns=['Inspector', 'Blocked Time', 'Simulation Time'])

    iProducts = pd.DataFrame(initialProduct, columns=['Product', 'Production Time'])
    iBlockedInspector = pd.DataFrame(initialInspectorB, columns=['Inspector', 'Blocked Time'])

    outputInspector(replica, blockedInspector, False)
    outputProduct(replica, products, False)
    outputInspector(replica, iBlockedInspector, True)
    outputProduct(replica, iProducts, True)

    initialBT.loc[replica] = totalBlockedTime(replica, iBlockedInspector, True)
    initialTP.loc[replica] = productThroughput(replica, iProducts, True)
    blockTimes.loc[replica] = totalBlockedTime(replica, blockedInspector, False)
    throughput.loc[replica] = productThroughput(replica, products, False)

    if replica == TOTAL_REPS:
        initialBT.loc[replica + 1] = 'Average:', initialBT['Total Blocked Time'].mean(), RUN_TIME
        initialTP.loc[replica + 1] = 'Average:',initialTP['Throughput(product/hour)'].mean(), RUN_TIME

        initialBT.loc[replica + 2] = 'Std:', initialBT['Total Blocked Time'].std(), RUN_TIME
        initialTP.loc[replica + 2] = 'Std:', initialTP['Throughput(product/hour)'].std(), RUN_TIME

        initialBT.loc[replica + 3] = 'CI:+-' + "{:.3f}".format(
            2.26 * (initialBT.iloc[replica + 1]['Total Blocked Time']) / math.sqrt(replica)), \
                                      initialBT.iloc[replica]['Total Blocked Time'] - (2.26 * (
                                      initialBT.iloc[replica + 1]['Total Blocked Time']) / math.sqrt(replica)), \
                                      initialBT.iloc[replica]['Total Blocked Time'] + (2.26 * (
                                      initialBT.iloc[replica + 1]['Total Blocked Time']) / math.sqrt(replica))

        initialTP.loc[replica + 3] = 'CI:+-' + "{:.5f}".format(
            2.26 * (initialTP.iloc[replica + 1]['Throughput(product/hour)']) / math.sqrt(replica)), \
                                      initialTP.iloc[replica]['Throughput(product/hour)'] - (2.26 * (
                                      initialTP.iloc[replica + 1]['Throughput(product/hour)']) / math.sqrt(replica)), \
                                      initialTP.iloc[replica]['Throughput(product/hour)'] + (2.26 * (
                                      initialTP.iloc[replica + 1]['Throughput(product/hour)']) / math.sqrt(replica))

        initialBT.loc[replica + 4] = 'PI:+-' + "{:.3f}".format(
            2.26 * initialBT.iloc[replica + 1]['Total Blocked Time'] * math.sqrt(1 + (1 / math.sqrt(replica)))), \
                                      initialBT.iloc[replica]['Total Blocked Time'] - (
                                                  2.26 * initialBT.iloc[replica + 1]['Total Blocked Time'] * math.sqrt(
                                              1 + (1 / math.sqrt(replica)))), \
                                      initialBT.iloc[replica]['Total Blocked Time'] + (
                                                  2.26 * initialBT.iloc[replica + 1]['Total Blocked Time'] * math.sqrt(
                                              1 + (1 / math.sqrt(replica))))

        initialTP.loc[replica + 4] = 'PI:+-' + "{:.5f}".format(
            2.26 * initialTP.iloc[replica + 1]['Throughput(product/hour)'] * math.sqrt(1 + (1 / math.sqrt(replica)))), \
                                      initialTP.iloc[replica]['Throughput(product/hour)'] - (
                                                  2.26 * initialTP.iloc[replica + 1][
                                              'Throughput(product/hour)'] * math.sqrt(1 + (1 / math.sqrt(replica)))), \
                                      initialTP.iloc[replica]['Throughput(product/hour)'] + (
                                                  2.26 * initialTP.iloc[replica + 1][
                                              'Throughput(product/hour)'] * math.sqrt(1 + (1 / math.sqrt(replica))))


        blockTimes.loc[replica + 1] = 'Average:', blockTimes['Total Blocked Time'].mean(), RUN_TIME - TO
        throughput.loc[replica + 1] = 'Average:', throughput['Throughput(product/hour)'].mean(), RUN_TIME - TO

        blockTimes.loc[replica + 2] = 'Std:', blockTimes['Total Blocked Time'].std(), RUN_TIME - TO
        throughput.loc[replica + 2] = 'Std:', throughput['Throughput(product/hour)'].std(), RUN_TIME - TO

        blockTimes.loc[replica + 3] = 'CI:+-' + "{:.3f}".format(2.26*(blockTimes.iloc[replica + 1]['Total Blocked Time'])/math.sqrt(replica)), \
                                      blockTimes.iloc[replica]['Total Blocked Time']-(2.26*(blockTimes.iloc[replica + 1]['Total Blocked Time'])/math.sqrt(replica)), \
                                      blockTimes.iloc[replica]['Total Blocked Time'] + (2.26 * (blockTimes.iloc[replica + 1]['Total Blocked Time']) / math.sqrt(replica))

        throughput.loc[replica + 3] = 'CI:+-' + "{:.5f}".format(2.26*(throughput.iloc[replica + 1]['Throughput(product/hour)'])/math.sqrt(replica)), \
                                      throughput.iloc[replica]['Throughput(product/hour)']-(2.26*(throughput.iloc[replica + 1]['Throughput(product/hour)'])/math.sqrt(replica)), \
                                      throughput.iloc[replica]['Throughput(product/hour)']+(2.26*(throughput.iloc[replica + 1]['Throughput(product/hour)'])/math.sqrt(replica))

        blockTimes.loc[replica + 4] = 'PI:+-' + "{:.3f}".format(2.26*blockTimes.iloc[replica + 1]['Total Blocked Time']*math.sqrt(1+(1/math.sqrt(replica)))), \
                                      blockTimes.iloc[replica]['Total Blocked Time']-(2.26*blockTimes.iloc[replica + 1]['Total Blocked Time']*math.sqrt(1+(1/math.sqrt(replica)))), \
                                      blockTimes.iloc[replica]['Total Blocked Time']+(2.26*blockTimes.iloc[replica + 1]['Total Blocked Time']*math.sqrt(1+(1/math.sqrt(replica))))

        throughput.loc[replica + 4] = 'PI:+-' + "{:.5f}".format(2.26*throughput.iloc[replica + 1]['Throughput(product/hour)']*math.sqrt(1+(1/math.sqrt(replica)))), \
                                      throughput.iloc[replica]['Throughput(product/hour)']-(2.26*throughput.iloc[replica + 1]['Throughput(product/hour)']*math.sqrt(1+(1/math.sqrt(replica)))), \
                                      throughput.iloc[replica]['Throughput(product/hour)']+(2.26*throughput.iloc[replica + 1]['Throughput(product/hour)']*math.sqrt(1+(1/math.sqrt(replica))))

    blockTimes.to_excel('Simulation_Block_Times.xlsx', index=False)
    throughput.to_excel('Simulation_Throughputs.xlsx', index=False)
    initialBT.to_excel('Initial_Simulation_Block_Times.xlsx', index=True)
    initialTP.to_excel('Initial_Simulation_Throughputs.xlsx', index=True)

if __name__ == "__main__":
    for r in range(1, TOTAL_REPS + 1):
        main(r)
