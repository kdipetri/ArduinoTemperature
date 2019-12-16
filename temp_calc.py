import numpy as np



def getTemp(resistance): 
    # * 
    # Function to calculate temperature for any resistance                                           
    # * 
    
    # Import values from https://ae01.alicdn.com/kf/HTB1ViBCdsUrBKNjSZPxq6x00pXa8/NTC-Thermistor-Accuracy-NTC-5k-3470-10k-3435-in-sensors-Temperature-Sensor-Waterproof-Probe-pipe-50mm.jpg
    x_temperature = np.linspace(-30, 30, num=61) #Points to be used for interpolation                 
    y_resistance  = np.array([88500,83200,78250,73600,69250,65200,61450,57900,54550,51450,48560,45830,43270,40860,38610,36490,34500,32630,30880,29230,27670,26210,24830,23540,22320,21170,20080,19060,18100,17190,16330,15520,14750,14030,13340,12700,12090,11510,10960,10440,9950,9485,9045,8630,8230,7855,7500,7160,6840,6535,6245,5970,5710,5460,5225,5000,4787,4583,4389,4204,4029])
    
    # Compute resistance from interpolation 
    temperature = np.interp(resistance, np.sort(y_resistance), -np.sort(x_temperature))
    
    # If debugging
    #plt.plot(x_temperature, y_resistance, 'o')                                                      
    #plt.show()                                                                                          
    return temperature 
