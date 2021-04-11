import pandas as pd
import math

eachProduct = pd.DataFrame(columns=['Replica', 'P1', 'P2', 'P3'])
blockTimes = pd.DataFrame(columns=['Replica', 'Total Blocked Time', 'TE'])
throughput = pd.DataFrame(columns=['Replica', 'Throughput(product/hour)', 'TE'])
initialBT = pd.DataFrame(columns=['Replica', 'Total Blocked Time', 'TE+TO'])
initialTP = pd.DataFrame(columns=['Replica', 'Throughput(product/hour)', 'TE+TO'])

class Calculations():
    def __init__(self, rep, RUN_TIME, TO):
        self.replicas = rep
        self.RUN_TIME = RUN_TIME
        self.TO = TO

    '''
    outputs the products onto a excel file 
    where each sheet is a separate simulation
    '''
    def outputInspector(self, replica, dataframe, initial):
        sheetName = 'Simulation_' + str(replica)
        if initial:
            if replica > 1:
                with pd.ExcelWriter('ExcelSheets/InitialBlockedInspectors.xlsx', mode='a') as writer:
                    dataframe.to_excel(writer, sheet_name=sheetName)
            else:
                with pd.ExcelWriter('ExcelSheets/InitialBlockedInspectors.xlsx') as writer:
                    dataframe.to_excel(writer, sheet_name=sheetName)
        else:
            if replica > 1:
                with pd.ExcelWriter('ExcelSheets/BlockedInspectors.xlsx', mode='a') as writer:
                    dataframe.to_excel(writer, sheet_name=sheetName)
            else:
                with pd.ExcelWriter('ExcelSheets/BlockedInspectors.xlsx') as writer:
                    dataframe.to_excel(writer, sheet_name=sheetName)

    '''
    outputs the products onto a excel file 
    where each sheet is a separate simulation
    '''
    def outputProduct(self, replica, dataframe, initial):
        sheetName = 'Simulation_' + str(replica)
        if initial:
            if replica > 1:
                with pd.ExcelWriter('ExcelSheets/InitialProductOutputs.xlsx', mode='a') as writer:
                    dataframe.to_excel(writer, sheet_name=sheetName)
            else:
                with pd.ExcelWriter('ExcelSheets/InitialProductOutputs.xlsx') as writer:
                    dataframe.to_excel(writer, sheet_name=sheetName)
        else:
            if replica > 1:
                with pd.ExcelWriter('ExcelSheets/ProductOutputs.xlsx', mode='a') as writer:
                    dataframe.to_excel(writer, sheet_name=sheetName)
            else:
                with pd.ExcelWriter('ExcelSheets/ProductOutputs.xlsx') as writer:
                    dataframe.to_excel(writer, sheet_name=sheetName)

    '''
    Calculates product throughput per/hour 
    '''
    def productThroughput(self, rep, dataframe, initial):
        if initial:
            return rep, len(dataframe.index) / (self.RUN_TIME / 60), self.RUN_TIME
        else:
            return rep, len(dataframe.index) / ((self.RUN_TIME - self.TO) / 60), self.RUN_TIME - self.TO

    '''
    Calculates the Total blocked time for each replica
    '''
    def totalBlockedTime(self, rep, dataframe, initial):
        if initial:
            return rep, dataframe['Blocked Time'].sum(), self.RUN_TIME
        else:
            return rep, dataframe['Blocked Time'].sum(), self.RUN_TIME - self.TO

    '''
    Calculates the average, standard deviation, CI, and PI of the blocked times
    '''
    def blockedCalc(self, dataframe, initial):
        if initial:
            dataframe.loc[self.replicas + 1] = 'Average:', dataframe[
                'Total Blocked Time'].mean(), self.RUN_TIME
            dataframe.loc[self.replicas + 2] = 'Std:', dataframe[
                'Total Blocked Time'].std(), self.RUN_TIME
        else:
            dataframe.loc[self.replicas + 1] = 'Average:', dataframe['Total Blocked Time'].mean(), self.RUN_TIME - self.TO
            dataframe.loc[self.replicas + 2] = 'Std:', dataframe['Total Blocked Time'].std(), self.RUN_TIME - self.TO

        dataframe.loc[self.replicas + 3] = 'CI:+-' + "{:.3f}".format(
            2.26 * (dataframe.iloc[self.replicas + 1]['Total Blocked Time']) / math.sqrt(self.replicas)), \
                                           dataframe.iloc[self.replicas]['Total Blocked Time'] - (2.26 * (
                                               dataframe.iloc[self.replicas + 1]['Total Blocked Time']) / math.sqrt(
                                               self.replicas)), \
                                           dataframe.iloc[self.replicas]['Total Blocked Time'] + (2.26 * (
                                               dataframe.iloc[self.replicas + 1]['Total Blocked Time']) / math.sqrt(
                                               self.replicas))
        dataframe.loc[self.replicas + 4] = 'PI:+-' + "{:.3f}".format(
            2.26 * dataframe.iloc[self.replicas + 1]['Total Blocked Time'] * math.sqrt(
                1 + (1 / math.sqrt(self.replicas)))), \
                                           dataframe.iloc[self.replicas]['Total Blocked Time'] - (
                                                   2.26 * dataframe.iloc[self.replicas + 1][
                                               'Total Blocked Time'] * math.sqrt(
                                               1 + (1 / math.sqrt(self.replicas)))), \
                                           dataframe.iloc[self.replicas]['Total Blocked Time'] + (
                                                   2.26 * dataframe.iloc[self.replicas + 1][
                                               'Total Blocked Time'] * math.sqrt(
                                               1 + (1 / math.sqrt(self.replicas))))

        if initial:
            dataframe.to_excel('ExcelSheets/Initial_Simulation_Block_Times.xlsx', index=True)
        else:
            dataframe.to_excel('ExcelSheets/Simulation_Block_Times.xlsx', index=False)

    '''
    Calculates the average, standard deviation, CI, and PI of the Throughputs
    '''
    def throughputCalc(self, dataframe, initial):
        if initial:
            dataframe.loc[self.replicas + 1] = 'Average:', dataframe[
                'Throughput(product/hour)'].mean(), self.RUN_TIME
            dataframe.loc[self.replicas + 2] = 'Std:', dataframe[
                'Throughput(product/hour)'].std(), self.RUN_TIME
        else:
            dataframe.loc[self.replicas + 1] = 'Average:', dataframe['Throughput(product/hour)'].mean(), self.RUN_TIME - self.TO
            dataframe.loc[self.replicas + 2] = 'Std:', dataframe['Throughput(product/hour)'].std(), self.RUN_TIME - self.TO

        dataframe.loc[self.replicas + 3] = 'CI:+-' + "{:.5f}".format(
            2.26 * (dataframe.iloc[self.replicas + 1]['Throughput(product/hour)']) / math.sqrt(self.replicas)), \
                                           dataframe.iloc[self.replicas]['Throughput(product/hour)'] - (2.26 * (
                                               dataframe.iloc[self.replicas + 1][
                                                   'Throughput(product/hour)']) / math.sqrt(self.replicas)), \
                                           dataframe.iloc[self.replicas]['Throughput(product/hour)'] + (2.26 * (
                                               dataframe.iloc[self.replicas + 1][
                                                   'Throughput(product/hour)']) / math.sqrt(self.replicas))

        dataframe.loc[self.replicas + 4] = 'PI:+-' + "{:.5f}".format(
            2.26 * dataframe.iloc[self.replicas + 1]['Throughput(product/hour)'] * math.sqrt(
                1 + (1 / math.sqrt(self.replicas)))), \
                                           dataframe.iloc[self.replicas]['Throughput(product/hour)'] - (
                                                   2.26 * dataframe.iloc[self.replicas + 1]
                                           ['Throughput(product/hour)'] * math.sqrt(
                                               1 + (1 / math.sqrt(self.replicas)))), \
                                           dataframe.iloc[self.replicas]['Throughput(product/hour)'] + (
                                                   2.26 * dataframe.iloc[self.replicas + 1]
                                           ['Throughput(product/hour)'] * math.sqrt(
                                               1 + (1 / math.sqrt(self.replicas))))

        if initial:
            dataframe.to_excel('ExcelSheets/Initial_Simulation_Throughputs.xlsx', index=True)
        else:
            dataframe.to_excel('ExcelSheets/Simulation_Throughputs.xlsx', index=False)

    '''
    Calculates the throughput of each product type
    '''
    def eachProductThroughput(self, rep, dataframe):
        p1 = dataframe[dataframe.Product == 'P1']
        p2 = dataframe[dataframe.Product == 'P2']
        p3 = dataframe[dataframe.Product == 'P3']
        eachProduct.loc[rep] = rep, len(p1.index) / (self.RUN_TIME / 60), len(p2.index) / (self.RUN_TIME / 60), \
                               len(p3.index) / (self.RUN_TIME / 60)
        if rep == self.replicas:
            eachProduct.to_excel('ExcelSheets/EachProductThroughput.xlsx', index=False)