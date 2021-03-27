from enum import Enum
from random import *

from Milestone3.Inspector import Inspector
from Milestone3.Random import Random
from Milestone3.Workstation import Workstation


class States(Enum):
    WAITING = 1
    BLOCKED = 2
    ASSEMBLING = 3


c1Times = Random("C1")
c2Times = Random("C2")
c3Times = Random("C3")
w1Times = Random("W1")
w2Times = Random("W2")
w3Times = Random("W3")

workS1 = Workstation(1, "C1", "", States.WAITING)
workS2 = Workstation(2, "C1", "C2", States.WAITING)
workS3 = Workstation(3, "C1", "C3", States.WAITING)

insp1 = Inspector(1, "C1", "", States.WAITING)
insp2 = Inspector(2, "C2", "C3", States.WAITING)


def simulator():
    processT1 = 0
    processT2 = 0
    processT3 = 0
    insp2TotalBTime = 0
    for i in range(0, 1000):
        if workS1.checkAssemble() and workS1.getState() == States.WAITING:
            processT1 = w1Times.getRand()
            p1 = workS1.assemble(processT1)
            print(p1.name, p1.processedTime)
            workS1.setState(States.ASSEMBLING)

        if workS2.checkAssemble() and workS2.getState() == States.WAITING:
            processT2 = w2Times.getRand()
            p2 = workS2.assemble(processT2)
            print(p2.name, p2.processedTime)
            workS2.setState(States.ASSEMBLING)

        if workS3.checkAssemble() and workS3.getState() == States.WAITING:
            processT3 = w3Times.getRand()
            p3 = workS3.assemble(processT3)
            print(p3.name, p3.processedTime)
            workS3.setState(States.ASSEMBLING)

        if insp1.state == States.WAITING:
            inspectTime1 = c1Times.getRand()
            c1 = insp1.inspect(inspectTime1, "C1")
            buf1 = workS1.checkBuffer("C1")
            buf2 = workS2.checkBuffer("C1")
            buf3 = workS3.checkBuffer("C1")
            if insp2.state == States.BLOCKED:
                insp2.timeBlocked(inspectTime1)

            if buf1 <= buf2 and buf1 <= buf3 and buf1 < 2:
                workS1.addComponent(c1)
                workS1.timeWaited(inspectTime1, "C1")
                workS2.timeWaited(inspectTime1, "C1")
                workS3.timeWaited(inspectTime1, "C1")
            elif buf2 < buf1 and buf2 <= buf3 and buf2 < 2:
                workS2.addComponent(c1)
                workS2.timeWaited(inspectTime1, "C1")
            elif buf3 < buf1 and buf3 < buf2 and buf3 < 2:
                workS3.addComponent(c1)
                workS3.timeWaited(inspectTime1, "C1")

        if insp2.state == States.WAITING:
            randC = randrange(2)
            if randC == 0:
                inspectTime2 = c2Times.getRand()
                c2 = insp2.inspect(inspectTime2, "C2")
                if workS2.checkBuffer("C2") < 2 or workS2.checkBuffer("C2") is None:
                    workS2.addComponent(c2)
                    workS2.timeWaited(inspectTime2, "C2")
                else:
                    insp2.setState(States.BLOCKED)
                    workS2.timeWaited(inspectTime2, "C2")
                    insp2.blockC = c2
            elif randC == 1:
                inspectTime2 = c3Times.getRand()
                c3 = insp2.inspect(inspectTime2, "C3")
                if workS3.checkBuffer("C3") < 2 or workS3.checkBuffer("C3") is None:
                    workS3.addComponent(c3)
                    workS3.timeWaited(inspectTime2, "C3")
                else:
                    insp2.setState(States.BLOCKED)
                    workS3.timeWaited(inspectTime2, "C3")
                    insp2.blockC = c3

        elif insp2.state == States.BLOCKED:
            if insp2.blockC.name == "C2":
                if workS2.checkBuffer("C2") < 2 or workS2.checkBuffer("C2") is None:
                    insp2.setState(States.WAITING)
                    workS2.addComponent(insp2.blockC)
                    workS2.timeWaited(insp2.blockC.startT + insp2.blockTime, "C2")
                    insp2TotalBTime += insp2.blockTime
                    insp2.blockTime = 0
            elif insp2.blockC.name == "C3":
                if workS3.checkBuffer("C3") < 2 or workS3.checkBuffer("C3") is None:
                    insp2.setState(States.WAITING)
                    workS3.addComponent(insp2.blockC)
                    workS3.timeWaited(insp2.blockC.startT + insp2.blockTime, "C3")
                    insp2TotalBTime += insp2.blockTime
                    insp2.blockTime = 0

        if inspectTime1 > processT1 and workS1.getState() == States.ASSEMBLING:
            workS1.setState(States.WAITING)
            processT1 = 0
        else:
            processT1 -= inspectTime1

        if inspectTime2 > processT2 and inspectTime1 > processT2 and workS2.getState() == States.ASSEMBLING:
            workS2.setState(States.WAITING)
            processT2 = 0
        else:
            if inspectTime2 > inspectTime1:
                processT2 -= inspectTime2
            else:
                processT2 -= inspectTime1

        if inspectTime2 > processT3 and inspectTime1 > processT3 and workS3.getState() == States.ASSEMBLING:
            workS3.setState(States.WAITING)
            processT3 = 0
        else:
            if inspectTime2 > inspectTime1:
                processT3 -= inspectTime2
            else:
                processT3 -= inspectTime1

simulator()