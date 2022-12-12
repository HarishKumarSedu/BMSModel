import os 
import sys

cwdPath = os.getcwd()
sys.path.append(r"{cwdPath}")

import pandas as pd 
from pandas import ExcelWriter
from pandas import ExcelFile
from datetime import datetime
import matplotlib.pyplot as plt
import time 

from PowerAnalyzer import PowerAnalyzer
# from MCP import MCP

class DataCollection:
    
    def __init__(self) -> None:
        
        self.powerAnalyzer = PowerAnalyzer()
        self._battSafeArea = True
        self._vBattCyclesCompleted = True
         
        self.SOC = [[],[],[],[],[],[],[],[]]
        self.vBatt = [[],[],[],[],[],[],[],[]]
        self.vBatt = [[],[],[],[],[],[],[],[]]
        self.voltages=[[],[],[],[],[],[],[],[]]
        self.currents=[[],[],[],[],[],[],[],[]]
        self.simDatetime=[]
        self.index = []
        
        #trigger the FPGA to start the balancing 
        # self.powerAnalyzer.triggerDCDC_Con()
        
        #set the DC Dc converter outPut shunt resistance 
        self.shuntResistance = 3e-3
        
        self.DCDCOutPutCurrent = []
        
    # def dctodcTrigger(self):
    #     self.powerAnalyzer.triggerDCDC_Con()
        
        #operate the DC/DC converter through the mcp
        # self.mcp = MCP()
        
    def dataCollect(self):
        try:
            #Chroma enable sequence 
            # self.mcp.chromaSwitchOnSequence()
            
            for i in range(1,400002):
                
                batVoltSOCs=self.powerAnalyzer.BattPack.batVoltageSOC()
                voltage=self.powerAnalyzer.BattPack.batEmulator.BateryEmulatorCellVoltages
                current=self.powerAnalyzer.BattPack.batEmulator.BateryEmulatorCellCurrent
                # print('Batt 0 Voltage')
                # print(voltage[0])
                # print(self.powerAnalyzer.BattPack.batEmulator.BateryEmulatorCellCurrent)
                
                #enable if any voltage measuremets in the setup
                # volt=self.powerAnalyzer.MeterView.voltMeter.volt()
                
                #Shunt current 
                
                # self.DCDCOutPutCurrent.append(self.powerAnalyzer.dcdcOutputShuntVoltage()/self.shuntResistance)
                
                volt = list(batVoltSOCs.keys())
                soc = list(batVoltSOCs.values())
                print('Batt 0 Voltage')
                print(volt[0])
                # if (min(volt) > 3.0 and max(volt) <= 4.2):
                # if (min(volt) >= 0.0 and max(volt) <= 4.2):
                if (min(soc) >= 0.05 and max(soc) <= 0.95):
                    if (i != 1):
                    
                        for j in range(0,len(volt)):
                            self.SOC[j].append(soc[j])
                            self.vBatt[j].append(volt[j])
                        for k in range(0,8):
                            self.voltages[k].append(voltage[k])
                            self.currents[k].append(current[k])
                        self.index.append(i)  
                        self.simDatetime.append(datetime.now())  
                    if(i%100 == 0):
                        print(f'{i} cycles are completed ')
                        # write to the excel sheet 
                        # batDf = pd.DataFrame({'Index':self.index,'Sim Date Time':self.simDatetime,'SOC7':self.SOC[0],'vBatt7':self.vBatt[0],'SOC6':self.SOC[1],'vBatt6':self.vBatt[1],'SOC5':self.SOC[2],'vBatt5':self.vBatt[2],'SOC4':self.SOC[3],'vBatt4':self.vBatt[3],'SOC3':self.SOC[4],'vBatt3':self.vBatt[4],'SOC2':self.SOC[5],'vBatt2':self.vBatt[5],'SOC1':self.SOC[6],'vBatt1':self.vBatt[6],'SOC0':self.SOC[7],'vBatt0':self.vBatt[7]})
                        batDf = pd.DataFrame({'Index':self.index,'Sim Date Time':self.simDatetime,'vBatt0':self.voltages[0],'CurrentBatt0':self.currents[0],'vBatt1':self.voltages[1],'CurrentBatt1':self.currents[1],'vBatt2':self.voltages[2],'CurrentBatt2':self.currents[2],'vBatt3':self.voltages[3],'vBatt4':self.voltages[4],'CurrentBatt4':self.currents[4],'vBatt5':self.voltages[5],'CurrentBatt5':self.currents[5],'vBatt6':self.voltages[6],'CurrentBatt6':self.currents[6],'vBatt7':self.voltages[7],'CurrentBatt7':self.currents[7]})
                        writer = ExcelWriter('Logs/BatStackDischargeSimulation.xlsx')
                        batDf.to_excel(writer,'Sheet1',index=False)
                        writer.save()

                    time.sleep(0.1)
                else:
                    print('Battery is in out of safety area ')
                    self.clearAll() # additional clear off for safety purpose
                    self._battSafeArea = False
                    
                    break
            self._vBattCyclesCompleted = False
            self.clearAll() # additional clear for the safety purpose 
            
        except KeyboardInterrupt:
            print(f'{i} cycles are completed ')
            # batDf = pd.DataFrame({'Index':self.index,'Sim Date Time':self.simDatetime,'SOC7':self.SOC[0],'vBatt7':self.vBatt[0],'SOC6':self.SOC[1],'vBatt6':self.vBatt[1],'SOC5':self.SOC[2],'vBatt5':self.vBatt[2],'SOC4':self.SOC[3],'vBatt4':self.vBatt[3],'SOC3':self.SOC[4],'vBatt3':self.vBatt[4],'SOC2':self.SOC[5],'vBatt2':self.vBatt[5],'SOC1':self.SOC[6],'vBatt1':self.vBatt[6],'SOC0':self.SOC[7],'vBatt0':self.vBatt[7]})
            batDf = pd.DataFrame({'Index':self.index,'Sim Date Time':self.simDatetime,'vBatt0':self.voltages[0],'CurrentBatt0':self.currents[0],'vBatt1':self.voltages[1],'CurrentBatt1':self.currents[1],'vBatt2':self.voltages[2],'CurrentBatt2':self.currents[2],'vBatt3':self.voltages[3],'vBatt4':self.voltages[4],'CurrentBatt4':self.currents[4],'vBatt5':self.voltages[5],'CurrentBatt5':self.currents[5],'vBatt6':self.voltages[6],'CurrentBatt6':self.currents[6],'vBatt7':self.voltages[7],'CurrentBatt7':self.currents[7]})
            writer = ExcelWriter('Logs/BatStackDischargeSimulation.xlsx')
            batDf.to_excel(writer,'Sheet1',index=False)
            writer.save()
            # self.clearAll()
            plt.plot(self.index,self.voltages[7],'-')
            plt.plot(self.index,self.voltages[0],'.')
            plt.xlabel('iterations x100ms ')
            plt.ylabel('Batt Voltage')
            plt.legend(["Batt7", "Batt0"], loc ="best")
            plt.show()
            
            #Chroma disable sequence 
            # self.mcp.chromaSwitchOffSequence()
            time.sleep(1)
            for i in range(0,8):
                self.powerAnalyzer.BattPack.batEmulator.batteryEmulatorVoltageSet(cellNo=i+1,cellVoltage=0)
            time.sleep(1)
            self.clearAll()
    def clearAll(self):
        self.SOC.clear()
        self.vBatt.clear()
        self.powerAnalyzer.BattPack.clearAll()
        
if __name__ == '__main__':
    dataCollection = DataCollection()
    # start = input('Start aquire data :')
    # if start == 'YES':
    #     # dataCollection.dctodcTrigger
    #     dataCollection.dataCollect()
    dataCollection.dataCollect()
    # dataCollection.clearAll()