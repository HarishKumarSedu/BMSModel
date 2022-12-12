

import pandas as pd 
import scipy.interpolate as interpolate

class BatteryParameters:
    
    def __init__(self):
        self._ROTC  = self.ROTCfunc()
        self._COTC  = self.COTCfunc()
        self._ROCH    = self.ROCHfunc()
        self._RODCH    = self.RODCHfunc()
        self._SOC    = self.SOCfunc()
        self._VOC    = self.VOCfunc()

    
    def VOCfunc(self):
        data = pd.read_csv('BMS_lookup_tables/Table_OCV_SOC_2.txt', sep=",",header=None,names=["SOC","VOCV"],dtype="float")
        VOC_Inter = interpolate.interp1d(data.SOC, data.VOCV, kind='cubic')
        return VOC_Inter
        
    def ROTCfunc(self):
        #Rdf = ROTC only 
        data = pd.read_csv('BMS_lookup_tables/Table_ROTC_SOC_v2.txt', sep=",",header=None,names=["SOC","Rdf"],dtype="float")
        ROTC_Inter = interpolate.interp1d(data.SOC, data.Rdf, kind='cubic')
        return ROTC_Inter
    
    def COTCfunc(self):
        #Cdf = CTOC only 
        data = pd.read_csv('BMS_lookup_tables/Table_COTC_SOC_v2.txt', sep=",",header=None,names=["SOC","Cdf"],dtype="float")
        COTC_Inter = interpolate.interp1d(data.SOC, data.Cdf, kind='cubic')
        return COTC_Inter
    
    def ROCHfunc(self):
        #Ro=Rin
        data = pd.read_csv('BMS_lookup_tables/Table_RCHG_SOC_v2.txt', sep=",",header=None,names=["SOC","RO"],dtype="float")
        RO_Inter = interpolate.interp1d(data.SOC, data.RO, kind='cubic')
        return RO_Inter

    def RODCHfunc(self):
        #Ro=Rin
        data = pd.read_csv('BMS_lookup_tables/Table_Rin_SOC_discharge.txt', sep=" ",header=None,names=["NAN1","SOC","NAN2","RO","NAN3"],dtype="float")
        data.drop(["NAN1","NAN2","NAN3"], axis=1, inplace=True)
        RO_Inter = interpolate.interp1d(data.SOC, data.RO, kind='cubic')
        return RO_Inter

    def SOCfunc(self):
        #Ro=Rin
        data = pd.read_csv('BMS_lookup_tables/Table_OCV_SOC_2.txt', sep=",",header=None,names=["SOC","VOCV"],dtype="float")
        SOC_Inter = interpolate.interp1d(data.VOCV, data.SOC, kind='cubic')
        return SOC_Inter
    
    @property
    def ROTC(self):
        return self._ROTC
    
    @property
    def COTC(self):
        return self._COTC
    
    @property
    def ROCH(self):
        return self._ROCH

    @property
    def RODCH(self):
        return self._RODCH

    @property
    def SOC(self):
        return self._SOC
    
    @property
    def VOC(self):
        return self._VOC
    
        
    
if __name__ == '__main__':
    BattModel = BatteryParameters()
    ROTC = BattModel.ROTC
    i=ROTC(4.166667E-3)
    COTC = BattModel.COTC
    j=COTC(4.166667E-3)
    ROCH = BattModel.ROCH
    m=ROCH(4.166667E-3)
    VOC = BattModel.VOC
    n=VOC(4.166667E-3)
    
    print(f'the soc 4.166667E-3 ROTC intepolation {i} \n  the soc COTC intepolation {j} \n the soc ROCH intepolation {m} \n VOC {n}' )