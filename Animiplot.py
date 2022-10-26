import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time 

class Animiplot:
    def __init__(self) -> None:
        
        self.fig, self.ax = plt.subplots()
        self.xdata, self.ydata = [], []
        self.xdata2,self.ydata2= [], []
        self.ln, = plt.plot([], [], 'ro') 
        self.ln2, = plt.plot([], [], 'ro')

    def init(self):
        self.ax.set_xlim(0, 2*np.pi)
        self.ax.set_ylim(-1, 1)
        return self.ln,self.ln2

    def update(self,frame):
        # print(frame)
        start_time = time.time()
        print(start_time)
        self.xdata.append(frame)
        self.ydata.append(np.sin(frame))
        self.ln.set_data(self.xdata, self.ydata)

        self.xdata2.append(frame)
        self.ydata2.append(np.cos(frame))
        self.ln2.set_data(self.xdata2,self.ydata2)
        print(time.time())
        
        return self.ln,self.ln2

if __name__ == '__main__':

    dataPlot = Animiplot()
    ani = FuncAnimation(dataPlot.fig, dataPlot.update, frames=np.linspace(0, 2*np.pi, 128),init_func=dataPlot.init, blit=True,interval=100)

    plt.show()