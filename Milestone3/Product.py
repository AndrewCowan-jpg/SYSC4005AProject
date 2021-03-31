class Product:
    def __init__(self, name, component1, component2):
        self.name = name
        self.component1 = component1
        self.component2 = component2
        
        self.totalTime = 0
        
    def calculateProductionTime(self, currentTime):
        earliestTime = 0
        if self.component2 is None:
            self.totalTime = currentTime - self.component1.startT
        else:    
            if self.component1.startT < self.component2.startT:
                earliestTime = self.component1.startT
            else:
                earliestTime = self.component2.startT
                
            self.totalTime = currentTime - earliestTime