
from Chroma import Chroma
from BatteryModel import BatteryModel
 
# 0.6,0.6,0.6,0.6,0.6,0.6,0.6,0.4
class BatteryPack:
    
    def __init__(self,Q_tot=10,dt=0.01,SOC0=[0.4,0.6,0.6,0.6,0.6,0.6,0.6,0.6],ibattBias=0,balancingNode=0) -> None:
        self.Q_tot = Q_tot
        self.dt = dt 
        self.SOC0 = SOC0
        self.currents = []
        self.Batt=[]
        self.ibattBias = ibattBias # default it is in charging bias current at the power analyzer leve
        self.batEmulator = Chroma(noOfBMStestingCells=len(self.SOC0)) # Battery emulator handle 
        self.ibattBias_2 = -3 # extra bias current at the pack level //// -ve for carging +ve for discharging
        
        self.node = balancingNode # biasing node / balancing node 
        
        for i in range(0,len(self.SOC0)):
            self.Batt.append(BatteryModel(Q_tot=self.Q_tot,SOC0=self.SOC0[i])) # create number of the Battery Model instances #8 for instance 
            
        
    def batVoltageSOC(self):
        batVoltSOC =dict()
        currents = self.batEmulator.BateryEmulatorCellCurrent
        # chromaCellVoltages = self.batEmulator.BateryEmulatorCellVoltages
        
        biasedCurrent = []
        SOC = []
        # print(f'Current that flowinf in Chroma {currents}')
        
        #add the sudo bias current 
        i=0
        for Current in reversed(currents):
            # the condition is just to simulate the particular node current for now 
            # Battery #1 get less current so the charging curve has larger slope compare to other batteries
            
            if i == self.node:
                biasedCurrent.append(Current+self.ibattBias + self.ibattBias_2)
                print('Batt0 current') 
                print(biasedCurrent[i])
            else:
                biasedCurrent.append(Current+self.ibattBias - self.ibattBias_2)

            # for normal operation enable
            # biasedCurrent.append(Current + self.ibattBias)
            i=i+1
            
        for i in range(0,len(self.SOC0)):
            [batVlot,VOC] = self.Batt[i].battVoltage(biasedCurrent[i])
            batVoltSOC[batVlot] = self.Batt[i].CoulombSOC
            # batVoltSOC[chromaCellVoltages[i]] = self.Batt[i].CoulombSOC
            self.batEmulator.batteryEmulatorVoltageSet(cellNo=i+1,cellVoltage=VOC)
            
        return batVoltSOC
        
    def clearAll(self):
        self.batEmulator.closeBatteryEmulator()
        
if __name__ == '__main__':
    battPack = BatteryPack()
    print('*'*50)
    print('Battery Pack')
    print(battPack.batVoltageSOC())
    print('*'*50)