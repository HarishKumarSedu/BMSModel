import os 
import sys

cwdPath = os.getcwd()
sys.path.append(r"{cwdPath}")

import pandas as pd 
from pandas import ExcelWriter
from pandas import ExcelFile
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np
import time 

from PowerAnalyzer import PowerAnalyzer

class DataCollection:
    
    def __init__(self) -> None:
        
        self.powerAnalyzer = PowerAnalyzer()
        self._battSafeArea = True
        self._vBattCyclesCompleted = True
         
        self.SOC = [[],[],[],[],[],[],[],[]]
        self.vBatt = [[],[],[],[],[],[],[],[]]
        self.simDatetime=[]
        self.index = []
        
    def dataCollect(self):
        for i in range(1,402):
            
            batVoltSOCs=self.powerAnalyzer.BattPack.batVoltageSOC()
            
            #enable if any voltage measuremets in the setup
            # volt=self.powerAnalyzer.MeterView.voltMeter.volt()
            
            volt = list(batVoltSOCs.keys())
            soc = list(batVoltSOCs.values())
            # if (min(volt) > 3.0 and max(volt) <= 4.2):
            # if (min(volt) >= 0.0 and max(volt) <= 4.2):
            if (min(soc) >= 0.05 and max(soc) <= 0.95):
                if (i != 1):
                
                    for j in range(0,len(volt)):
                        self.SOC[j].append(soc[j])
                        self.vBatt[j].append(volt[j])
                        
                    self.index.append(i)  
                    self.simDatetime.append(datetime.now())  
                if(i%100 == 0):
                    print(f'{i} cycles are completed ')
                    # print(self.vBatt[1])
                    # print(self.SOC[1])
                    # write to the excel sheet 
                    batDf = pd.DataFrame({'Index':self.index,'Sim Date Time':self.simDatetime,'SOC0':self.SOC[0],'vBatt0':self.vBatt[0],'SOC1':self.SOC[1],'vBatt1':self.vBatt[1],'SOC2':self.SOC[2],'vBatt2':self.vBatt[2],'SOC3':self.SOC[3],'vBatt3':self.vBatt[3],'SOC4':self.SOC[4],'vBatt4':self.vBatt[4],'SOC5':self.SOC[5],'vBatt5':self.vBatt[5],'SOC6':self.SOC[6],'vBatt6':self.vBatt[6],'SOC7':self.SOC[7],'vBatt7':self.vBatt[7]})
                    writer = ExcelWriter('Logs/BatStackDischargeSimulation.xlsx')
                    batDf.to_excel(writer,'Sheet1',index=False)
                    writer.save()
                    # plt.plot(self.SOC[1],self.vBatt[1])
                    # plt.xlabel('soc ')
                    # plt.ylabel('Volt')
                    # plt.show()
                    
                time.sleep(0.1)
            else:
                print('Battery is in out of safety area ')
                self.clearAll() # additional clear off for safety purpose
                self._battSafeArea = False
                
                break
        self._vBattCyclesCompleted = False
        self.clearAll() # additional clear for the safety purpose 
    
    def dataSend(self):
        batVoltSOCs=self.powerAnalyzer.BattPack.batVoltageSOC()
            
            #enable if any voltage measuremets in the setup
            # volt=self.powerAnalyzer.MeterView.voltMeter.volt()
            
        volt = list(batVoltSOCs.keys())
        soc = list(batVoltSOCs.values())
        # if (min(volt) > 3.0 and max(volt) <= 4.2):
        # if (min(volt) >= 0.0 and max(volt) <= 4.2):
        # for j in range(0,len(volt)):
        #     self.SOC[j].append(soc[j])
        #     self.vBatt[j].append(volt[j])
                        
        #     # self.index.append(i) 
        return volt
    def clearAll(self):
        self.SOC.clear()
        self.vBatt.clear()
        self.powerAnalyzer.BattPack.clearAll()
        
class Dataplot:
    
    def __init__(self,N=1) -> None:
        self.N=N
        self.fig, self.ax = plt.subplots()
        self.iterations = []
        self.vBatt = [[],[],[],[],[],[],[],[]]
        self.vbatt1 = []
        self.ln1, = plt.plot([], [], 'ro') 
        self.ln2, = plt.plot([], [], 'ro')
        self.ln3, = plt.plot([], [], 'ro') 
        self.ln4, = plt.plot([], [], 'ro')
        self.ln5, = plt.plot([], [], 'ro') 
        self.ln6, = plt.plot([], [], 'ro')
        self.ln7, = plt.plot([], [], 'ro') 
        self.ln8, = plt.plot([], [], 'ro')

    def init(self):
        self.ax.set_xlim(0, 1000)
        self.ax.set_ylim(0, 4.2)
        
        return self.ln1,self.ln2,self.ln3,self.ln4,self.ln5,self.ln6,self.ln7,self.ln8,
    
    def update(self,frame):
        print(frame)
        self.vbatt1.append(frame)

        self.ln1.set_data(range(len(self.vbatt1)),self.vbatt1)
        return self.ln1
    
    def anime(self):
        return animation.FuncAnimation(self.fig, self.update, frames=np.linspace(0, 2*np.pi, 128),init_func=self.init, blit=True,interval=100)
    
        
        
if __name__ == '__main__':
    
    
    dataCollection = DataCollection()
    # dataCollection.dataCollect()
    # dataCollection.clearAll()
    
    dataPlot = Dataplot()
    # dataPlot.anime()
    ani=animation.FuncAnimation(dataPlot.fig, dataPlot.update, frames=dataCollection.dataSend(),init_func=dataPlot.init, blit=True,interval=100)
    plt.show()