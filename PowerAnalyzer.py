

from BatteryPack import BatteryPack
from LoadCharger import LoadCharger
from MeterView import MeterView

class PowerAnalyzer:
    
    def __init__(self) -> None:
        
        self.BattPack = BatteryPack(ibattBias=0) # for -ve batteries are charging , +ve batteries are discharging
        self.LoadCharger = LoadCharger()
        # self.MeterView = MeterView()
        
    def triggerDCDC_Con(self):
        self.MeterView.trigger.TogglePin24()
        
    def dcdcOutputShuntVoltage(self):
        return self.MeterView.voltMeter.Volt()