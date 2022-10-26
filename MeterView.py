

from Digilent import Digilent

from VoltMeter import mul_34461A
from Digilent import Digilent

class MeterView:
    
    def __init__(self) -> None:
        self.voltMeter = mul_34461A()
        self.trigger = Digilent()