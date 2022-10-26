#! /usr/bin/env python3

"""Demonstrate the use of the DigitalIO functionality."""

import time
import argparse
import random

from pydwf import DwfLibrary, PyDwfError
from pydwf.utilities import openDwfDevice
from ctypes import *    # It provides C compatible data types, and allows calling functions in DLLs or shared libraries
from sys import path    # This is needed to check the OS type and get the PATH
from os import sep      # OS specific file path separators
import time

#-------------------------------------------------------------------------------
# Initialization
#-------------------------------------------------------------------------------

constants_path = "C:" + sep + "Program Files (x86)" + sep + "Digilent" + sep + \
                 "WaveFormsSDK" + sep + "samples" + sep + "py"

# import constants
path.append(constants_path)
from dwfconstants import *


class Digilent:
    
    def __init__(self) -> None:
        # load the dynamic library, get constants path (the path is OS specific)
        self.dwf = cdll.dwf

        # Device hardware handle
        self.hdwf = c_int()
        dwRead = c_uint32()

        version = create_string_buffer(32)
        self.dwf.FDwfGetVersion(version)
        print("DWF Version: " + str(version.value))

        print("Opening first device")
        self.dwf.FDwfDeviceOpen(c_int(-1), byref( self.hdwf))

        if  self.hdwf.value == hdwfNone.value:
            print("failed to open device")
            szerr = create_string_buffer(512)
            self.dwf.FDwfGetLastErrorMsg(szerr)
            print(str(szerr.value))
            quit()
            
        self.dwf.FDwfDigitalIOOutputEnableSet( self.hdwf, c_int(0x0001))
        
    def TogglePin24(self):
        # input("Press Enter to toggle DIO24...")
        
        self.dwf.FDwfDigitalIOOutputSet( self.hdwf, c_int(0x0001))
        time.sleep(100e-3)
        self.dwf.FDwfDigitalIOOutputSet( self.hdwf, c_int(0x0000))
        # time.sleep(1e-3)
        
if __name__ == "__main__":
    digilent = Digilent()
    digilent.TogglePin24()