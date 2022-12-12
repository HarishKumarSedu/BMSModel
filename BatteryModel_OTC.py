import numpy as np
from BatteryParameters_OTC import BatteryParameters

class BatteryModel:
    
    def __init__(self,Q_tot=10,dt=0.1,SOC0=0.8) -> None:
        self.Q_tot      = Q_tot
        self.dt         = dt 
        self.SOC        = SOC0
        self.BatTable   = BatteryParameters()
        self.ibatt      = 0.0
        self._VOTC      = 0.0
        self.RO         = 0.0
       
    def battVoltage(self,ibatt):
        self.RO    = self.BatTable.ROCH(self.SOC)
        self.VOC   = self.BatTable.VOC(self.SOC)
        self.Vbatt = self.VOC - self.VOTC - self.RO*self.ibatt
        self.ibatt = ibatt
        return [self.Vbatt,self.VOC]
        
  
    @property
    def VOTC(self)->float:
        self._VOTC = self._VOTC * np.exp(-self.dt /(self.BatTable.COTC(self.SOC) * self.BatTable.ROTC(self.SOC) )) +  self.BatTable.ROTC(self.SOC) * ( 1 - np.exp(-self.dt /(self.BatTable.COTC(self.SOC) * self.BatTable.ROTC(self.SOC) ))) * self.ibatt
        return self._VOTC
    
    @property
    def CoulombSOC(self):
        self.SOC = self.SOC - self.ibatt * self.dt /(self.Q_tot * 3600)
        return self.SOC
        

    def batteryCurrentUpdate(self,ibatt):
        self.ibatt = ibatt
        
if __name__ == '__main__':
    Batt = BatteryModel()
    ibatt = 1 # Battery current 
    Batt.batteryCurrentUpdate(ibatt)
    print('Battery Voltage and the open Circuit Voltage ')
    print(Batt.battVoltage(ibatt))
    print('Updated SOC')
    print(Batt.CoulombSOC)
    