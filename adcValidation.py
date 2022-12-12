from operator import index
from Chroma import Chroma
import serial

import pandas as pd 
from pandas import ExcelWriter
from pandas import ExcelFile

class adcValidation:
    
    def __init__(self,port="COM5",baudrate=115200) -> None:
        self.port = port 
        self.baudrate = baudrate
        self.serial = serial.Serial(self.port,self.baudrate)
        self.chroma = Chroma(noOfBMStestingCells=0,initVoltage=0.0)
        
        
    def setVoltage(self,voltage):
        self.chroma.batteryEmulatorVoltageSet(1,voltage)
    
    def readBatteryEmulatorVoltage(self):
        return self.chroma.BateryEmulatorCellVoltages
    
    def readBLEdata(self):
        data = []
        for i in range(1,1000):
            val = self.serial.readline().decode();
            print(val);
            #data.append(int())
        #return  sum(data)/len(data)
        return 0
    
    
if __name__ == '__main__':
     adcValid = adcValidation()
     voltageSet = 2.0
     ChromaVoltage = []
     BLEvoltage = []
     index= []
     input('Run scritp')
     for i in range(1,1000):
         voltageSet = voltageSet + 0.001
         adcValid.setVoltage(voltageSet)
         ChromaVoltage.append(adcValid.readBatteryEmulatorVoltage)
         BLEvoltage.append(adcValid.readBLEdata)
         index.append(i)
    # batDf = pd.DataFrame({'Index':index , 'BLEvoltage' : BLEvoltage,'ChromaVoltage':ChromaVoltage})
    # writer = ExcelWriter('Logs/adcValidation.xlsx')
    # batDf.to_excel(writer,'Sheet1',index=False)
    # writer.save()
        