
from Chroma import Chroma
# from BatteryModel_OTC import BatteryModel # Switch the model according to the application requirement 
from BatteryModel_TTC import BatteryModel
import matplotlib.pyplot as plt
from MCP import MCP
import time 

from itertools import pairwise

class BatteryPack:

# battery socs from top to bottom in order 
#Bottom cell ->0.5,0.9,0.9,0.9,0.9,0.9,0.9,0.9 -> Top cell
    
    def __init__(self,Q_tot=10,dt=0.01,SOC0=[0.9,0.9,0.9,0.9,0.9,0.9,0.8,0.9],ibattBias=0,balancingNode=None) -> None:
        self.Q_tot = Q_tot
        self.dt = dt 
        self.SOC0 = SOC0
        self.currents = []
        self.Batt=[]
        self.ibattBias = ibattBias # default it is in charging bias current at the power analyzer leve
        self.batEmulator = Chroma(noOfBMStestingCells=len(self.SOC0)) # Battery emulator handle 
        self.ibattBias_2 = 0 # extra bias current at the pack level //// -ve for carging +ve for discharging
        
        self.node = balancingNode # biasing node / balancing node 
       
        for i in range(0,len(self.SOC0)):
            self.Batt.append(BatteryModel(Q_tot=self.Q_tot,SOC0=self.SOC0[i])) # create number of the Battery Model instances #8 for instance 
            
        
    def batVoltageSOC(self):
        batVoltSOC =dict()
        currents = self.batEmulator.BateryEmulatorCellCurrent
        biasedCurrent = []
        SOC = []
        
        #add the sudo bias current 
        for i in range(0,len(self.SOC0)):

            if currents[i] > 0 :
                biasedCurrent.append(currents[i]+self.ibattBias+self.ibattBias_2)
            elif currents[i] < 0 :
                biasedCurrent.append(currents[i]-self.ibattBias - self.ibattBias_2)
            else:
                biasedCurrent.append(0)

            # for normal operation enable
            # biasedCurrent.append(Current + self.ibattBias)

        for i in range(0,len(self.SOC0)):
            ''' Debugging Purpose'''
            
            print(biasedCurrent[i])
            [batVlot,VOC] = self.Batt[i].battVoltage(biasedCurrent[i])
            batVoltSOC[batVlot] = self.Batt[i].CoulombSOC
            self.batEmulator.batteryEmulatorVoltageSet(cellNo=len(self.SOC0)-i,cellVoltage=batVlot)
        return batVoltSOC
        
    def clearAll(self):
        self.batEmulator.closeBatteryEmulator()
        
if __name__ == '__main__':
    battPack = BatteryPack()
    print('*'*50)
    print('Battery Pack')
    print('*'*50)
    voltages=[[],[],[],[],[],[],[],[]]
    battPack.batVoltageSOC()
    for i in range(1,400200):
        try:
            volts=battPack.batEmulator.BateryEmulatorCellVoltages
            print(volts)
            delta = [y-x for (x, y) in pairwise([volts[0],volts[1]])]
            if False:#abs(max(delta)) < 0.0002:
                print('Cell Balanced')
                break
            else:
                battPack.batVoltageSOC()
                for i in range(0,len(volts)):
                    voltages[i].append(volts[i])
            time.sleep(0.1)
        except KeyboardInterrupt:
            for i in range(0,8):
                battPack.batEmulator.batteryEmulatorVoltageSet(cellNo=i+1,cellVoltage=0)
            time.sleep(1)
            battPack.batEmulator.closeBatteryEmulator()
            break

    