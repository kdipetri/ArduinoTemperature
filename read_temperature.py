import argparse
import pyfirmata
import datetime
import time
import matplotlib.pyplot as plt 
from matplotlib.animation import FuncAnimation


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

def getTimestamp():
		datetime_str = datetime.datetime.now()  
		return datetime_str

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

class tempMeasurement():

	def __init__(self):

		# board 
		self.board = pyfirmata.Arduino(board_location)
	
		# analog pinx
		self.analog_inputs = []

		self.npins = 6

		# arrays for plotting
		self.timestamps = []
		self.temps = [ [] for pin in range(self.npins) ]
		self.lines = [ [] for pin in range(self.npins) ]
	
		# output
		self.file_name = "{}/{}.txt".format(output_directory,datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))

	def initializeBoard(self):

		it = pyfirmata.util.Iterator(self.board)
		it.start()

	def addAnalogInputs(self):

		for pin in range(0,self.npins):
			self.analog_inputs.append( self.board.get_pin('a:{}:i'.format(pin) ) )


	def getTemperatures(self): 
	
		# * 
		# Read ADC Value for Analog Pin, sample multiple times
		# *
		adcVals = [0]*self.npins
		for i in range (0,num_samples):
			for pin in range(0,self.npins):
				time.sleep(0.1)
				adcVal_tmp = self.analog_inputs[pin].read()
				adcVals[pin] = adcVals[pin] + adcVal_tmp 
				#print("(pin,ADC) ({},{})".format(pin,adcVal_tmp))
		
		# note: in pyfirmata reading analog pins returns a decimal between 0 and 1, where 1 is max value 
		
		# * 
		# Compute resistance and temp 
		# * 
		R = [0]*self.npins
		T = [0]*self.npins
		for pin in range(0,self.npins):
		
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

	def updateTempArrays(self,T):
	
		for pin in range(0,self.npins):
			self.temps[pin].append(T[pin]) 
		

	def updateTimestampArray(self,timestamp):
		
		self.timestamps.append(timestamp)
		
	def saveOutput(self,timestamp,T):
		f = open(self.file_name, 'a')
		f.write("{} {:.1f} {:.1f} {:.1f} {:.1f} {:.1f} {:.1f}\n".format(timestamp, T[0],T[1],T[2],T[3],T[4],T[5] ))
		f.close()

	def datePlot( self):
		if len(self.timestamps) == 1: 
		    figure = plt.figure()
		    plt.ioff()
		    plt.autoscale(enable=True, axis='both', tight=True)
		    self.lines[0], = plt.plot(self.timestamps,self.temps[0], label="T0")
		    self.lines[1], = plt.plot(self.timestamps,self.temps[1], label="T1")
		    self.lines[2], = plt.plot(self.timestamps,self.temps[2], label="T2")
		    self.lines[3], = plt.plot(self.timestamps,self.temps[3], label="T3")
		    self.lines[4], = plt.plot(self.timestamps,self.temps[4], label="T4")
		    self.lines[5], = plt.plot(self.timestamps,self.temps[5], label="T5")
		    plt.xlabel("Time") 
		    plt.ylabel("Temp [C]") 
		    plt.gcf().autofmt_xdate()
		    plt.legend()
		    #plt.show()
		else : 
		    self.lines[0].set_data(self.timestamps,self.temps[0])
		    self.lines[1].set_data(self.timestamps,self.temps[1])
		    self.lines[2].set_data(self.timestamps,self.temps[2])
		    self.lines[3].set_data(self.timestamps,self.temps[3])
		    self.lines[4].set_data(self.timestamps,self.temps[4])
		    self.lines[5].set_data(self.timestamps,self.temps[5])
		    
		    plt.xlim(self.timestamps[0],self.timestamps[-1])
		    plt.ylim(min([min(temp) for temp in self.temps])-2, max([max(temp) for temp in self.temps])+2)
		    plt.gcf().autofmt_xdate()
		    #plt.draw()
		    plt.savefig("currentTemp.png")
		    plt.pause(0.1)
		
		#return lines
			

	def finish(self):

		print("")
		print("Exiting")
		print("")
		print("Data saved in {}".format(self.file_name)) 
		print("")
		plot_filename_pdf = "plots/{}.pdf".format(self.file_name.split("/")[1])
		plt.savefig(plot_filename_pdf)

# * 
# Main
# * 


def main():

	# * 
	# Initilize class
	# * 
	meas = tempMeasurement()
	meas.initializeBoard()
	meas.addAnalogInputs()

	print("To stop program enter Ctrl+C")

	try : 
		while True : 
		
			time.sleep(1.0) 
			
			timestamp,T = meas.getTemperatures()
			
			# * 
			# Save output to text file
			# *
			meas.saveOutput(timestamp,T)
			
			# *
			# Update monitoring plot
			# * 
			meas.updateTempArrays(T)
			meas.updateTimestampArray(timestamp)
			meas.datePlot()

	except KeyboardInterrupt:

		# ends loop with Ctrl+C
		#f.close()
		meas.finish()
		

  
if __name__== "__main__":
	main()









