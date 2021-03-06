import argparse
import pyfirmata
import datetime
import time
import matplotlib.pyplot as plt 
import numpy as np
from matplotlib.animation import FuncAnimation


# *
# Argument parsing
# *
parser = argparse.ArgumentParser(description="Temperature measurement with ArduinoUno voltage divider")
parser.add_argument('-o' , '--output_directory'  , dest='output_directory' , help='directory for saving text files with temp'   , required=False   , default = 'output' )
parser.add_argument('-b' , '--board_location'    , dest='board_location'   , help='location of ArduinoUno, usually "/dev/xxxx"' , required=False   , default='/dev/ttyACM1' )
parser.add_argument('-n' , '--num_samples'       , dest='num_samples'      , help='number of samples per ADC measurement'       , required=False   , default = 5   )
parser.add_argument('-t' , '--thermistors'       , dest='thermistors'      , help='array of different thermistors'              , required=False   , default = ["10kPTC","5kNTC","5kNTC","5kNTC","5kNTC","5kNTC"])
parser.add_argument('-r' , '--resistors'         , dest='resistors'        , help='array of resistor values , in ohms'          , required=False   , default = [10000, 4700, 4700, 4700, 4700, 4700] )

args = parser.parse_args()

output_directory  = args.output_directory
board_location    = args.board_location #can be found from Arduino IDE which scans USB ports
num_samples       = args.num_samples
thermistors       = args.thermistors
resistors         = args.resistors

def getTimestamp():
		datetime_str = datetime.datetime.now()  
		return datetime_str

def getTemp5kNTC(resistance): 
    # * 
    # Function to calculate temperature for any resistance, using 5k thermistor                                           
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

def resistance_calc_10kPTC(T):
    # *
    # Function to calculate resistance for temp using 10k PTC thermistor
    # * 
    R0 = 100 # 
    alpha = 0.00385
    Delta = 1.4999 # for pure platinum?
    if T < 0: 
        Beta = 0.10863
    else : Beta = 0
    RT = (R0 + R0*alpha*(T - Delta*(T/100.-1)*(T/100.) - Beta*(T/100. - 1)*((T/100)**3)))*100
    return RT
    
def getTemp10kPTC(resistance): 
    # * 
    # Function to calculate temperature for any resistance, using 10k thermistor                       
    # * 
    #x_temperature = np.array([-50,-40,-30,-20,-10,0,10,20,25,30,40,50,60,70,80,90,100,110,120,130]) #Points to be used for interpolation                 
    #y_resistance  = np.array([8030.6,8427.1,8822.2,9216,9608.6,10000,10390.3,10779.4,10973.5,11167.3,11554.1,11939.7,12324.2,12707.5,13089.7,13470.7,13850.6,14229.3,14606.8,14983.2])
    x_temperature = np.linspace(-30,30, num=61) #Points to be used for interpolation                 
    #y_resistance  = np.array([176683,166091,156199,146959,138332,130243,122687,115613,108991,102787,96974,91525,86415,81621,77121,72895,68927,65198,61693,58397,55298,5252380,49633,47047,44610,42314,40149,38108,36182,34366,32650,31030,29500,28054,26687,25395,24172,23016,21921,20885,19903,18973,18092,17257,16465,15714,15001,14324,13682,13052,12493,11943,11420,10922,10449,10000,9572,9164,8777,8407,8056])
    #y_resistance = np.array([8822,8862,8901,8940,8980,9019,9059,9098,9137,9177,9216,9255,9295,9334,9373,9412,9452,9491,9530,9569,9609,9648,9687,9726,9765,9804,9844,9883,9922,9961,10000,10039,10078,10117,10156,10195,10234,10273,10312,10351,10390,10429,10468,10507,10546,10585,1010624,10663,10702,10740,10779,10818,10857,10896,10935,10973,11012,11051,11090,11129,11167])
    y_resistance = np.array([])
    for i in range(len(x_temperature)):
        y_resistance = np.append(y_resistance,resistance_calc_10kPTC(x_temperature[i]))
    

    temperature = np.interp(resistance, y_resistance, x_temperature)
    
    #print(resistance, temperature)
    # If debugging
    #plt.plot(x_temperature, y_resistance, 'o')                                                      
    #plt.show()   

    return temperature 

def getTemp(resistance,opt="5kNTC"):

    if   opt=="5kNTC"   : return getTemp5kNTC(resistance) 
    elif opt=="10kPTC"  : return getTemp10kPTC(resistance)
    else                : return 30

class tempMeasurement():

	def __init__(self):

		# board 
		self.board = pyfirmata.Arduino(board_location)
	
		# analog pins
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
			else : R[pin] = resistors[pin] * ( 1.0 / float(adcVals[pin]) - 1.00 )
		
			# temp
			T[pin] = getTemp(R[pin],thermistors[pin])

			#if pin < 1 : print("(pin,ADC,R,T) ({},{},{},{})".format(pin,adcVals[pin],R[pin],T[pin]))
		
		
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
			
			figure = plt.figure(dpi=200)
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
		    plt.draw()
		    plt.savefig("currentTemp.png")
		    time.sleep(0.1)
		
		#return lines
			

	def finish(self):

		print("")
		print("Exiting")
		print("")
		print("Data saved in {}".format(self.file_name)) 
		print("")
		plot_filename_pdf = "plots/{}.pdf".format(self.file_name.split("/")[1].strip(".txt"))
		plt.savefig(plot_filename_pdf)

# * 
# Main
# * 


def main():

	# * 
	# Initilize class
	# * 
    #thermistors        = ["10kPTC","5kPTC","5kNTC","5kNTC","5kNTC"]
    #series_resistors   = [10000   , 4700  , 4700  , 4700  , 4700  ]
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









