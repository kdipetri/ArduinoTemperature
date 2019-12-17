import argparse
import pyfirmata
import datetime
import time
import matplotlib.pyplot as plt 
from matplotlib.animation import FuncAnimation
from temp_calc import * 


# *
# Argument parsing
# *
parser = argparse.ArgumentParser(description="Temperature measurement with ArduinoUno voltage divider")
parser.add_argument('-o' , '--output_directory'            , dest='output_directory'     , help='directory for saving text files with temp'              , required=False   , default = 'output' )
parser.add_argument('-b' , '--board_location'              , dest='board_location'       , help='location of ArduinoUno, usually "/dev/xxxx"'            , required=False   , default='/dev/cu.usbmodem1421' )
parser.add_argument('-n' , '--num_samples'                 , dest='num_samples'          , help='number of samples per ADC measurement'                  , required=False   , default = 5   )
parser.add_argument('-r' , '--series_resistance'           , dest='series_resistance'    , help='value of resistor in series with thermistor, in ohms'   , required=False   , default = 4700 )

args = parser.parse_args()

output_directory  = args.output_directory
board_location    = args.board_location #can be found from Arduino IDE which scans USB ports
num_samples       = args.num_samples
series_resistance = args.series_resistance

# * 
# Setup board and analog pins
# * 
board = pyfirmata.Arduino(board_location)

it = pyfirmata.util.Iterator(board)
it.start()

analog_inputs = []
analog_inputs.append( board.get_pin('a:0:i') )
analog_inputs.append( board.get_pin('a:1:i') )
analog_inputs.append( board.get_pin('a:2:i') )
analog_inputs.append( board.get_pin('a:3:i') )
analog_inputs.append( board.get_pin('a:4:i') )
analog_inputs.append( board.get_pin('a:5:i') )

npins = len(analog_inputs) 

def getTimestamp():
    datetime_str = datetime.datetime.now()  
    return datetime_str

def getTemperatures(): 

  # * 
  # Read ADC Value for Analog Pin, sample multiple times
  # *
  adcVals = [0]*npins
  for i in range (0,num_samples):
     for pin in range(0,npins):
        time.sleep(0.1)
        adcVal_tmp = analog_inputs[pin].read()
        adcVals[pin] = adcVals[pin] + adcVal_tmp 
        #print("(pin,ADC) ({},{})".format(pin,adcVal_tmp))

  # note: in pyfirmata reading analog pins returns a decimal between 0 and 1, where 1 is max value 
 
  # * 
  # Compute resistance and temp 
  # * 
  R = [0]*npins
  T = [0]*npins
  for pin in range(0,npins):
  
    # finish averaging  
    adcVals[pin] = adcVals[pin]/num_samples
    
    # resistance
    if adcVals[pin] == 0 : R[pin] = 0
    else : R[pin] = series_resistance * ( 1.0 / float(adcVals[pin]) - 1.00 )

    # temp
    T[pin] = getTemp(R[pin])

  
  # debug
  timestamp = getTimestamp()
  print("{} (T0,T1,T2,T3,T4,T5) ( {:.1f}, {:.1f}, {:.1f}, {:.1f}, {:.1f}, {:.1f} )".format(timestamp,T[0],T[1],T[2],T[3],T[4],T[5] )) 

  return timestamp, T 

def updateTempArrays( tempArrays, Tmeas):

  for pin in range(0,npins):
    tempArrays[pin].append(Tmeas[pin]) 

  return tempArrays

def updatePlot( times, temps, lines ):
    if len(times) == 1: 
        figure = plt.figure()
        plt.ion()
        plt.autoscale(enable=True, axis='both', tight=True)
        lines[0], = plt.plot(times,temps[0], label="T0")
        lines[1], = plt.plot(times,temps[1], label="T1")
        lines[2], = plt.plot(times,temps[2], label="T2")
        lines[3], = plt.plot(times,temps[3], label="T3")
        lines[4], = plt.plot(times,temps[4], label="T4")
        lines[5], = plt.plot(times,temps[5], label="T5")
        plt.xlabel("Time") 
        plt.ylabel("Temp [C]") 
        plt.gcf().autofmt_xdate()
        plt.legend()
        #plt.show()
    else : 
        lines[0].set_data(times,temps[0])
        lines[1].set_data(times,temps[1])
        lines[2].set_data(times,temps[2])
        lines[3].set_data(times,temps[3])
        lines[4].set_data(times,temps[4])
        lines[5].set_data(times,temps[5])
        
        plt.xlim(times[0],times[-1])
        plt.ylim(min([min(temp) for temp in temps])-2, max([max(temp) for temp in temps])+2)
        plt.gcf().autofmt_xdate()
        plt.draw()
        plt.pause(0.1)
    
    return lines
    #plt.savefig("currentTemp.png")

    

# * 
# Main
# * 

# get start time for output file name
file_name = "{}/{}.txt".format(output_directory,datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))

# print out helpful info
print("To stop program enter Ctrl+C")

# initialize arrays for plotting
timestamps = []
Tarray = [ [] for pin in range(npins) ]
lines = [ [] for pin in range(npins) ]

#animation = FuncAnimation(figure, updatePlot(timestamps,Tarray), interval=10)

try : 
  while True : 
  
    time.sleep(1.0) 
  
    timestamp,T = getTemperatures()
  
    # * 
    # Save output to text file
    # *
    f = open(file_name, 'a')
    f.write("{} {:.1f} {:.1f} {:.1f} {:.1f} {:.1f} {:.1f}\n".format(timestamp, T[0],T[1],T[2],T[3],T[4],T[5] ))
    f.close()
    
    # *
    # Update monitoring plot
    # * 
    Tarray = updateTempArrays(Tarray, T)
    timestamps.append(timestamp)
    lines = updatePlot(timestamps,Tarray,lines)

except KeyboardInterrupt:

    # ends loop with Ctrl+C
    #f.close()

    print("")
    print("Exiting")
    print("")
    print("Data saved in {}".format(file_name)) 
    print("")


