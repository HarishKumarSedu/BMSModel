import time

import pyvisa as visa
from pyvisa.attributes import *
from pyvisa.constants import *
import matplotlib.pyplot as plt

class mul_34461A:

    def __init__(self, usb_id='USB0::0x2A8D::0x1301::MY57216238::INSTR'):
        rm = visa.ResourceManager()
        self.my_instr = rm.open_resource(usb_id)
        self.my_instr.read_termination = '\n'
        self.my_instr.write_termination = '\n'
        # self.meas_V() # set if voltage measure range set 
        self.my_instr.write('VOLT:DC:NPLC 0.02') # set NPLC to speed up the measuremtns 
        
    def get_IDN(self):
        return (self.my_instr.query('*IDN?'))

    def reset(self):
        self.my_instr.write('*RST')     

    def get_error(self):
        return self.my_instr.query('SYST:ERR?')  


    def read_value(self, cnt):
        self.my_instr.write(':SAMP:COUN ' + str(cnt) +';:TRIG:SOUR IMM')      
        data_str= self.my_instr.query(':READ?')
        data_split = data_str.split(sep =',')
        value = list(map(float, data_split))
        return(sum(value) / len(value))

    def meas_V(self, range = -1, count = 4):
        self.my_instr.write(':FUNC "VOLT:DC"') 
        #Range: Autorange (-1), 100 mV, 1 V, 10 V, 100 V, or 750 V
        range_list = [-1, 0.1, 1, 10, 100, 750]
        if range in range_list:
            range_auto = ':VOLT:DC:RANG:AUTO '
            range_val = ';:VOLT:DC:RANG '
            res_com = ';:VOLT:DC:RES '

            if range == -1:
                range_auto_cmd = 'ON'
                range_val = ''
                range_val_str = ''
                res_com = ''
                res_val_str = ''
            else:
                range_auto_cmd = 'OFF'
                range_val_str = str(range)
                if range == 0.1 or range == 1:
                    res = 1e-6
                elif range == 10:
                    res = 1e-5
                elif range == 100:
                    res = 1e-4    
                else:   
                    res = 1e-3
                res_val_str = str(res)

            com = range_auto + range_auto_cmd +  range_val + range_val_str + res_com + res_val_str
            self.my_instr.write(com) 
            self.my_instr.write('VOLT:IMP:AUTO ON')
            array = []
            while count>0:
                if count > 4:
                    cnt = 4
                else:
                    cnt = count 
                array.append(self.read_value(cnt))
                count -= 4 
            return(sum(array)/len(array))   
        else:
            return('ERR: Wrong range')   

    

    def meas_I(self, range = -1, count = 4):
        self.my_instr.write(':FUNC "CURR:DC"') 
        #Range: : Autorange (-1), 100 µA, 1 mA, 10 mA, 100 mA, 1 A, 3 A, or 10 A
        range_list = [-1, 100e-6, 1e-3, 0.01, 0.1, 1, 3]
        if range in range_list:
            range_auto = ':CURR:DC:RANG:AUTO '
            range_val = ';:CURR:DC:RANG '
            res_com = ';:CURR:DC:RES '

            if range == -1:
                range_auto_cmd = 'ON'
                range_val = ''
                range_val_str = ''
                res_com = ''
                res_val_str = ''
            else:
                range_auto_cmd = 'OFF'
                range_val_str = str(range)
                if range in list([100e-6, 1e-3]):
                    res = 1e-9
                elif range == 10e-3:
                    res = 1e-8
                elif range == 100e-3:
                    res = 1e-7   
                elif range == 1:
                    res = 1e-6
                else:   
                    res = 1e-5
                res_val_str = str(res)

            com = range_auto + range_auto_cmd +  range_val + range_val_str + res_com + res_val_str
            self.my_instr.write(com) 
            #self.my_instr.write('VOLT:IMP:AUTO ON')
            array = []
            while count>0:
                if count > 4:
                    cnt = 4
                else:
                    cnt = count 
                array.append(self.read_value(cnt))
                count -= 4 
            return(sum(array)/len(array))   
        else:
            return('ERR: Wrong range')    
        
    def Volt(self):
        return float(self.my_instr.query('READ?'))       

if __name__ == '__main__':
    
    voltage=[]
    multimeter = mul_34461A()
    print('Capacitor voltage measuremtn started....')
    while True:
        try:
            voltage.append(multimeter.Volt())
        except KeyboardInterrupt:
            plt.plot(voltage)
            plt.xlabel('iterations')
            plt.ylabel('Capacitor Voltage')
            plt.show()
            break