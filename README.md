
Code to monitor temperature with ArduinoUno

# Setup 
* Can readout 5 thermistors at once, two options for each voltage divider 
    - 10k Thermistor connected in series with 10k resistor
    - 5k Thermistor is connected in series with 4.7k resistor 
* 5V applied across resistors 
* Resistance of thermistor can be measured with analog pin of Arduino (ADC)
* Resistance is convered to a temperature measurement
* A separate script can be used to plot temperature v. time 

# monitor.html 
  * Shows currentTemp.png 
  * Autoupdates every 10 seconds

# read_temperature.py 
  * Inputs
    - board location
    - analog pin
    - series resistor value
    - output directory 
    - number of samples (default 5)
  * Reads analog pin voltage
  * Converts voltage to resistance of thermistor 
  * Converts resistance to temperature 
  * Saves output to a text file throughout measurement
  * Autoupdates currentTemp.png for monitoring 
  * Also saves plot of temp v. time at end of measurement 
  * To stop script hit Ctrl+C

# temp_plot.py
  * Incase plot isn't made 
  * Inputs
    - file
  * Plots temp. v. time
  * Autoformated!


# Helpful
  * location of arduino is usually /dev/ttyACM*
  * will need to do the following as root if its been disconnected
  * $ usermod -a -G dialout daq
  * note that ADC measurement should be of the voltage across fixed resistor, with respect to ground
