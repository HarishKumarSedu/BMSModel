from USBridge import UsbBridge
from PyMCP2221A import PyMCP2221A

import time


class MCP:
    
    def __init__(self) -> None:
        
        
        self.connect(True,1)
        
    
    def connect(self, do_connect: bool, speed_idx: int, devnum = 0):
        if do_connect:
            self.mcp2221 = PyMCP2221A.PyMCP2221A(devnum = devnum)
            # self.reset()
            self.mcp2221 = PyMCP2221A.PyMCP2221A(devnum = devnum)
            self.gpioInit()
            self.dacInit()
            
        else:
            self.mcp2221 = PyMCP2221A.PyMCP2221A()
            # self.reset()
            self.gpioInit()
            self.dacInit()
    def reset(self):
        self.mcp2221.Reset()
        
    def gpioInit(self):
        self.mcp2221.GPIO_Init()
        self.mcp2221.GPIO_0_OutputMode()
        self.mcp2221.GPIO_1_OutputMode()
        self.mcp2221.GPIO_2_OutputMode()
        self.mcp2221.GPIO_3_OutputMode()
        
    def dacInit(self):
        self.mcp2221.DAC_2_Init()
        
    def LTC4231Enable(self):
        self.mcp2221.GPIO_0_Output(1)
    
    def LTC4231Disable(self):
        self.mcp2221.GPIO_0_Output(0)  # type: ignore
        
    def ISETaSET(self,value=0x10):
        self.mcp2221.DAC_Datawrite(value)  # type: ignore
        
    def ISETaDisable(self):
        self.mcp2221.DAC_Datawrite(0x00)  # type: ignore
        
    def LM5170Enable(self):
        self.mcp2221.GPIO_1_Output(1)
    
    def LM5170Disable(self):
        self.mcp2221.GPIO_1_Output(0)
        
    def LM5170EnableBuck(self):
        self.mcp2221.GPIO_3_Output(1)
    
    def LM5170EnableBoost(self):
        self.mcp2221.GPIO_3_Output(0)
    
    def chromaSwitchOnSequence(self):
        # time.sleep(1)
        self.LTC4231Enable()
        # time.sleep(1)
        self.ISETaSET()
        self.LM5170EnableBuck()
        self.LM5170Enable()
        
    def chromaSwitchOffSequence(self):
        self.ISETaDisable()
        self.LM5170Disable()
        self.LM5170EnableBoost()
        time.sleep(0.01)
        # time.sleep(1)
        self.LTC4231Disable()
        # time.sleep(1)
        
if __name__ == '__main__':
    mcp=MCP()
    print('*'*20)
    # mcp.chromaSwitchOnSequence()
    # mcp.chromaSwitchOffSequence()
    for i in range(0,0xff,1):
        print(i)
        mcp.ISETaSET(i)
        time.sleep(1)