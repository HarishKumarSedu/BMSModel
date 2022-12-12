
import pandas as pd 
import scipy.interpolate as interpolate

class BatteryParameters:
    
    def __init__(self):
        self._RTTC1ch  = self.RTTC1chfunc()
        self._CTTC1ch  = self.CTTC1chfunc()
        self._RTTC2ch  = self.RTTC2chfunc()
        self._CTTC2ch  = self.CTTC2chfunc()
        self._RTTC1dch  = self.RTTC1dchfunc()
        self._CTTC1dch  = self.CTTC1dchfunc()
        self._RTTC2dch  = self.RTTC2dchfunc()
        self._CTTC2dch  = self.CTTC2dchfunc()
        self._ROCH    = self.ROchfunc()
        # self._RODCH    = self.ROdchfunc()
        self._SOC    = self.SOCfunc()
        self._VOC    = self.VOCfunc()

    
    def VOCfunc(self):
        data = pd.read_csv('NMC53Ah/Interpolated/Table_OCV_SOC_NMC53Ah_int.txt', sep=",",header=None,names=["SOC","VOCV"],dtype="float")
        VOC_Inter = interpolate.interp1d(data.SOC, data.VOCV, kind='cubic')
        return VOC_Inter
        
    def RTTC1chfunc(self): 
        data = pd.read_csv('NMC53Ah/Interpolated/Table_RTTC1_SOC_NMC53Ah_chg_int.txt', sep=",",header=None,names=["SOC","RTTC1ch"],dtype="float")
        RTTC1ch_Inter = interpolate.interp1d(data.SOC, data.RTTC1ch, kind='cubic')
        return RTTC1ch_Inter
    
    def CTTC1chfunc(self):
        data = pd.read_csv('NMC53Ah/Interpolated/Table_CTTC1_SOC_NMC53Ah_chg_int.txt', sep=",",header=None,names=["SOC","CTTC1ch"],dtype="float")
        CTTC1ch_Inter = interpolate.interp1d(data.SOC, data.CTTC1ch, kind='cubic')
        return CTTC1ch_Inter
    
    def RTTC2chfunc(self): 
        data = pd.read_csv('NMC53Ah/Interpolated/Table_RTTC2_SOC_NMC53Ah_chg_int.txt', sep=",",header=None,names=["SOC","RTTC2ch"],dtype="float")
        RTTC2ch_Inter = interpolate.interp1d(data.SOC, data.RTTC2ch, kind='cubic')
        return RTTC2ch_Inter
    
    def CTTC2chfunc(self):
        data = pd.read_csv('NMC53Ah/Interpolated/Table_CTTC2_SOC_NMC53Ah_chg_int.txt', sep=",",header=None,names=["SOC","CTTC2ch"],dtype="float")
        CTTC2ch_Inter = interpolate.interp1d(data.SOC, data.CTTC2ch, kind='cubic')
        return CTTC2ch_Inter
    
    def RTTC1dchfunc(self): 
        data = pd.read_csv('NMC53Ah/Interpolated/Table_RTTC1_SOC_NMC53Ah_dischg_int.txt', sep=",",header=None,names=["SOC","RTTC1dch"],dtype="float")
        RTTC1dch_Inter = interpolate.interp1d(data.SOC, data.RTTC1dch, kind='cubic')
        return RTTC1dch_Inter
    
    def CTTC1dchfunc(self):
        data = pd.read_csv('NMC53Ah/Interpolated/Table_CTTC1_SOC_NMC53Ah_dischg_int.txt', sep=",",header=None,names=["SOC","CTTC1dch"],dtype="float")
        CTTC1dch_Inter = interpolate.interp1d(data.SOC, data.CTTC1dch, kind='cubic')
        return CTTC1dch_Inter
    
    def RTTC2dchfunc(self): 
        data = pd.read_csv('NMC53Ah/Interpolated/Table_RTTC2_SOC_NMC53Ah_dischg_int.txt', sep=",",header=None,names=["SOC","RTTC2dch"],dtype="float")
        RTTC2dch_Inter = interpolate.interp1d(data.SOC, data.RTTC2dch, kind='cubic')
        return RTTC2dch_Inter
    
    def CTTC2dchfunc(self):
        data = pd.read_csv('NMC53Ah/Interpolated/Table_CTTC2_SOC_NMC53Ah_dischg_int.txt', sep=",",header=None,names=["SOC","CTTC2dch"],dtype="float")
        CTTC2dch_Inter = interpolate.interp1d(data.SOC, data.CTTC2dch, kind='cubic')
        return CTTC2dch_Inter
    
    def ROchfunc(self):
        data = pd.read_csv('NMC53Ah/Interpolated/Table_R0_SOC_NMC53Ah_chg_int.txt', sep=",",header=None,names=["SOC","ROch"],dtype="float")
        ROch_Inter = interpolate.interp1d(data.SOC, data.ROch, kind='cubic')
        return ROch_Inter

    def ROdchfunc(self):
        data = pd.read_csv('NMC53Ah/Interpolated/Table_R0_SOC_NMC53Ah_dischg_int.txt', sep=" ",header=None,names=["SOC","ROdch"],dtype="float")
        ROdch_Inter = interpolate.interp1d(data.SOC, data.ROdch, kind='cubic')
        return ROdch_Inter

    def SOCfunc(self):
        data = pd.read_csv('NMC53Ah/Interpolated/Table_OCV_SOC_NMC53Ah_int.txt', sep=",",header=None,names=["SOC","VOCV"],dtype="float")
        SOC_Inter = interpolate.interp1d(data.VOCV, data.SOC, kind='cubic')
        return SOC_Inter
    
    @property
    def RTTC1ch(self):
        return self._RTTC1ch
    
    @property
    def CTTC1ch(self):
        return self._CTTC1ch
    
    @property
    def RTTC2ch(self):
        return self._RTTC1ch
    
    @property
    def CTTC2ch(self):
        return self._CTTC1ch
    
    @property
    def RTTC1dch(self):
        return self._RTTC1dch
    
    @property
    def CTTC1dch(self):
        return self._CTTC1dch
    
    @property
    def RTTC2dch(self):
        return self._RTTC1dch
    
    @property
    def CTTC2dch(self):
        return self._CTTC1dch
    
    @property
    def ROCH(self):
        return self._ROCH

    # @property
    # def RODCH(self):
    #     return self._RODCH

    @property
    def SOC(self):
        return self._SOC
    
    @property
    def VOC(self):
        return self._VOC
    
        
    
if __name__ == '__main__':
    BattModel = BatteryParameters()
    RTTC1 = BattModel.RTTC1dch
    i=RTTC1(4.166667E-3)
    CTTC1 = BattModel.CTTC1dch
    j=CTTC1(4.166667E-3)
    RTTC2 = BattModel.RTTC2dch
    k=RTTC2(4.166667E-3)
    CTTC2 = BattModel.CTTC2dch
    l=CTTC2(4.166667E-3)
    ROCH = BattModel.ROCH
    m=ROCH(4.166667E-3)
    VOC = BattModel.VOC
    n=VOC(4.166667E-3)
    
    print(f'the soc 4.166667E-3 RTTC1 and RTTC2 intepolation {i} {k} \n  the soc CTTC1 and CTTC2 intepolation {j} {l}\n the soc ROCH intepolation {m} \n VOC {n}' )