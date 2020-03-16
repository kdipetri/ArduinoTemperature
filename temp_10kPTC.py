import matplotlib.pyplot as plt 
import numpy as np

def tempPlot():

    
    x_temperature = np.array([-50,-40,-30,-20,-10,0,10,20,25,30,40,50,60,70,80,90,100,110,120,130]) #Points to be used for interpolation                 
    y_resistance  = np.array([8030.6,8427.1,8822.2,9216,9608.6,10000,10390.3,10779.4,10973.5,11167.3,11554.1,11939.7,12324.2,12707.5,13089.7,13470.7,13850.6,14229.3,14606.8,14983.2])

    plt.plot(x_temperature, y_resistance, 'o')                                                      
    plt.show()   
    #plt.savefig("temp10kPTC.png")

    return

tempPlot()

