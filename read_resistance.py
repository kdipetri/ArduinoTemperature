import argparse
import pyfirmata
import datetime
import time
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
  
def getResistance(): 

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
  # Compute resistance 
  # * 
  R = [0]*npins
  for pin in range(0,npins):
    
    adcVals[pin] = adcVals[pin]/num_samples
    if adcVals[pin] == 0 : R[pin] = 0
    else : R[pin] = series_resistance * ( 1.0 / float(adcVals[pin]) - 1.00 )

  # debug
  #print("{} (R0,R1,R2,R3,R4,R5) ({:.1f} , {:.1f} , {:.1f}, {:.1f}, {:.1f} )".format(datetime.datetime.now(),R[0], R[1], R[2], R[3], R[4], R[5] )) 
  print("{} (T0,T1,T2,T3,T4,T5) ({:.1f} , {:.1f} , {:.1f}, {:.1f}, {:.1f} )".format(datetime.datetime.now(),getTemp(R[0]), getTemp(R[1]), getTemp(R[2]), getTemp(R[3]), getTemp(R[4]), getTemp(R[5]) )) 

  return R 

# * 
# Main
# * 

# get start time for output file name
file_name = "{}/{}.txt".format(output_directory,datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))
f = open(file_name, 'w')

# print out helpful info
print("To stop program enter Ctrl+C")

try : 
  while True : 
  
    time.sleep(1.0) 
  
    R = getResistance()
  
    #print(resistance) 
    f.write("{} {:.1f} {:.1f} {:.1f} {:.1f} {:.1f} {:.1f}\n".format(datetime.datetime.now(), getTemp(R[0]), getTemp(R[1]), getTemp(R[2]), getTemp(R[3]), getTemp(R[4]), getTemp(R[5]) ))

except KeyboardInterrupt:

    # ends loop with Ctrl+C
    f.close()

    print("")
    print("Exiting")
    print("")
    print("Data saved in {}".format(file_name)) 
    print("")


