
Code to monitor temperature with ArduinoUno

5k Thermistor is connected in series with 4.7k resistor (voltage divider)
5V applied across resistors 
Resistance of thermistor can be measured with analog pin of Arduino (ADC)
Resistance is convered to a temperature measurement
A separate script can be used to plot temperature v. time 


read_temperature.py 
  # Inputs
    * board location
    * analog pin
    * series resistor value
    * output directory 
    * number of samples (default 10)
  # Reads analog pin voltage
  # Converts voltage to resistance of thermistor 
  # Converts resistance to temperature 
  # To stop script hit Ctrl+C

plot_temperature.py
  # Inputs
    * file
  # Plots temp. v. time
