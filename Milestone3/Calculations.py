import pandas as pd
import math

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
                with pd.ExcelWriter('InitialBlockedInspectors.xlsx', mode='a') as writer:
                    dataframe.to_excel(writer, sheet_name=sheetName)
            else:
                with pd.ExcelWriter('InitialBlockedInspectors.xlsx') as writer:
                    dataframe.to_excel(writer, sheet_name=sheetName)
        else:
            if replica > 1:
                with pd.ExcelWriter('BlockedInspectors.xlsx', mode='a') as writer:
                    dataframe.to_excel(writer, sheet_name=sheetName)
            else:
                with pd.ExcelWriter('BlockedInspectors.xlsx') as writer:
                    dataframe.to_excel(writer, sheet_name=sheetName)

    '''
    outputs the products onto a excel file 
    where each sheet is a separate simulation
    '''
    def outputProduct(self, replica, dataframe, initial):
        sheetName = 'Simulation_' + str(replica)
        if initial:
            if replica > 1:
                with pd.ExcelWriter('initialProductOutputs.xlsx', mode='a') as writer:
                    dataframe.to_excel(writer, sheet_name=sheetName)
            else:
                with pd.ExcelWriter('initialProductOutputs.xlsx') as writer:
                    dataframe.to_excel(writer, sheet_name=sheetName)
        else:
            if replica > 1:
                with pd.ExcelWriter('productOutputs.xlsx', mode='a') as writer:
                    dataframe.to_excel(writer, sheet_name=sheetName)
            else:
                with pd.ExcelWriter('productOutputs.xlsx') as writer:
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

    def blockedCalc(self, dataframe, initial):
        dataframe.loc[self.replicas + 1] = 'Average:', dataframe['Total Blocked Time'].mean(), self.RUN_TIME
        dataframe.loc[self.replicas + 2] = 'Std:', dataframe['Total Blocked Time'].std(), self.RUN_TIME
        dataframe.loc[self.replicas + 3] = 'CI:+-' + "{:.3f}".format(
            2.26 * (dataframe.iloc[self.replicas + 1]['Total Blocked Time']) / math.sqrt(self.replicas)), \
                                           dataframe.iloc[self.replicas]['Total Blocked Time'] - (2.26 * (
                                     dataframe.iloc[self.replicas + 1]['Total Blocked Time']) / math.sqrt(self.replicas)), \
                                           dataframe.iloc[self.replicas]['Total Blocked Time'] + (2.26 * (
                                     dataframe.iloc[self.replicas + 1]['Total Blocked Time']) / math.sqrt(self.replicas))
        dataframe.loc[self.replicas + 4] = 'PI:+-' + "{:.3f}".format(
            2.26 * dataframe.iloc[self.replicas + 1]['Total Blocked Time'] * math.sqrt(1 + (1 / math.sqrt(self.replicas)))), \
                                     dataframe.iloc[self.replicas]['Total Blocked Time'] - (
                                             2.26 * dataframe.iloc[self.replicas + 1]['Total Blocked Time'] * math.sqrt(
                                         1 + (1 / math.sqrt(self.replicas)))), \
                                     dataframe.iloc[self.replicas]['Total Blocked Time'] + (
                                             2.26 * dataframe.iloc[self.replicas + 1]['Total Blocked Time'] * math.sqrt(
                                         1 + (1 / math.sqrt(self.replicas))))
        if initial:
            dataframe.to_excel('Initial_Simulation_Block_Times.xlsx', index=True)
        else:
            dataframe.to_excel('Simulation_Block_Times.xlsx', index=False)

    def throughputCalc(self, dataframe, initial):
        dataframe.loc[self.replicas + 1] = 'Average:', dataframe['Throughput(product/hour)'].mean(), self.RUN_TIME
        dataframe.loc[self.replicas + 2] = 'Std:', dataframe['Throughput(product/hour)'].std(), self.RUN_TIME
        dataframe.loc[self.replicas + 3] = 'CI:+-' + "{:.5f}".format(
            2.26 * (dataframe.iloc[self.replicas + 1]['Throughput(product/hour)']) / math.sqrt(self.replicas)), \
                                           dataframe.iloc[self.replicas]['Throughput(product/hour)'] - (2.26 * (
                                     dataframe.iloc[self.replicas + 1]['Throughput(product/hour)']) / math.sqrt(self.replicas)), \
                                           dataframe.iloc[self.replicas]['Throughput(product/hour)'] + (2.26 * (
                                     dataframe.iloc[self.replicas + 1]['Throughput(product/hour)']) / math.sqrt(self.replicas))

        dataframe.loc[self.replicas + 4] = 'PI:+-' + "{:.5f}".format(
            2.26 * dataframe.iloc[self.replicas + 1]['Throughput(product/hour)'] * math.sqrt(1 + (1 / math.sqrt(self.replicas)))), \
                                     dataframe.iloc[self.replicas]['Throughput(product/hour)'] - (
                                             2.26 * dataframe.iloc[self.replicas + 1]
                                           ['Throughput(product/hour)'] * math.sqrt(1 + (1 / math.sqrt(self.replicas)))), \
                                     dataframe.iloc[self.replicas]['Throughput(product/hour)'] + (
                                             2.26 * dataframe.iloc[self.replicas + 1]['Throughput(product/hour)'] * math.sqrt(
                                               1 + (1 / math.sqrt(self.replicas))))
        if initial:
            dataframe.to_excel('Initial_Simulation_Throughputs.xlsx', index=True)
        else:
            dataframe.to_excel('Simulation_Throughputs.xlsx', index=False)
