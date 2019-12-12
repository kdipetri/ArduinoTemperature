import argparse
import pyfirmata
import time


# *
# Argument parsing
# *
parser = argparse.ArgumentParser(description="Temperature measurement with ArduinoUno voltage divider")
parser.add_argument('-o' , '--output_directory'            , dest='output_directory'     , help='directory for saving text files with temp'              , required=False   , default = 'output' )
parser.add_argument('-b' , '--board_location'              , dest='board_location'       , help='location of ArduinoUno, usually "/dev/xxxx"'            , required=False   , default='/dev/cu.usbmodem1421' )
parser.add_argument('-p' , '--analog_pin'                  , dest='analog_pin'           , help='analog pin which reads voltage across thermister, int'  , required=False   , default = 1    )           
parser.add_argument('-n' , '--num_samples'                 , dest='num_samples'          , help='number of samples per ADC measurement'                  , required=False   , default = 10   )
parser.add_argument('-r' , '--series_resistance'           , dest='series_resistance'    , help='value of resistor in series with thermistor, in ohms'   , required=False   , default = 4700 )

args = parser.parse_args()

output_directory  = args.output_directory
board_location    = args.board_location #can be found from Arduino IDE which scans USB ports
analog_pin        = args.analog_pin
num_samples       = args.num_samples
series_resistance = args.series_resistance

# * 
# Setup board and analog pin
# * 
board = pyfirmata.Arduino(board_location)

it = pyfirmata.util.Iterator(board)
it.start()

analog_input = board.get_pin('a:{}:i'.format(analog_pin))
  
def getResistance(): 

  # * 
  # Read ADC Value for Analog Pin, sample multiple times
  # *
  adcVal = 0
  for i in range (0,num_samples):
     adcVal = adcVal + analog_input.read() 
     time.sleep(0.1)

  adcVal = adcVal/num_samples
  # note: in pyfirmata reading analog pins returns a decimal between 0 and 1, where 1 is max value 
 
  # * 
  # Compute resistance 
  # * 
 
  resist = series_resistance * ( 1.0 / float(adcVal) - 1.00 ) 

  return resist


while True : 

  time.sleep(1.0) 

  resistance = getResistance()

  print(resistance) 


