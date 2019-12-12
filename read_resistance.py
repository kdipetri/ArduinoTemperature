import pyfirmata
import time

#Can use Arduino IDE to find board's location
board = pyfirmata.Arduino('/dev/cu.usbmodem1421')

it = pyfirmata.util.Iterator(board)
it.start()

##
## Initialize important values
##
analogPin = 1  # replace with analog pin
adcMax = 1023.00 # Arduino uses 10-bit ADC 
numSamples = 10
R0 = 4700. # Resistor in series = 4.7 kOhm 

analog_input = board.get_pin('a:1:i')
  
def getResistance(): 

  # * 
  # Read ADC Value for Analog Pin, sample multiple times
  # *
  adcVal = 0
  for i in range (0,numSamples):
     adcVal = adcVal + analog_input.read() 
     time.sleep(0.1)

  adcVal = adcVal/numSamples
  
  # * 
  # Compute resistance 
  # * 
 
  resist = R0 * ( 1.0 / float(adcVal) - 1.00 ) 

  return resist


while True : 

  time.sleep(1.0) 

  resistance = getResistance()

  print(resistance) 



