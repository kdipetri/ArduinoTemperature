import argparse
import datetime
import numpy as np
import matplotlib.pyplot as plt 
from numpy import loadtxt



# *
# Argument parsing
# *
parser = argparse.ArgumentParser(description="Make pretty plots of Arduino temperature measurement")
parser.add_argument('-i' , '--input_textfile'              , dest='input_textfile'       , help='input text file'              , required=False   , default ='output/2019-12-17_13:39:32.txt' )
parser.add_argument('-p' , '--plot_directory'              , dest='plot_directory'       , help='where plot will be saved'     , required=False   , default ='plots'   )

args = parser.parse_args()

input_textfile  = args.input_textfile
plot_directory  = args.plot_directory 

# *
# Input output processing 
# * 
plot_file = "{}}/{}.pdf".format(plot_directory,input_textfile.split("/")[1])

# * 
# Load text from file
# * 
datetimes = []
temps0    = []
temps1    = []
temps2    = []
temps3    = []
temps4    = []
temps5    = []
for line in open(txt_file,"r").readlines():

    # get infos
    date   = line.split()[0]
    time   = line.split()[1]
    temp0  = float(line.split()[2])
    temp1  = float(line.split()[3])
    temp2  = float(line.split()[4])
    temp3  = float(line.split()[5])
    temp4  = float(line.split()[6])
    temp5  = float(line.split()[7])

    # format datetime obj
    datetime_str = "{} {}".format(date,time)
    datetime_obj = datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S.%f')

    # append
    datetimes.append(datetime_obj)
    temps0.append(temp0)
    temps1.append(temp1)
    temps2.append(temp2)
    temps3.append(temp3)
    temps4.append(temp4)
    temps5.append(temp5)

    # debug
    print(datetime_obj, temp0, temp1, temp2, temp3, temp4, temp5)
 
# * 
# plot
# * 
plt.xlabel("Time") 
plt.ylabel("Temp [C]") 
plt.plot(datetimes,temps0, label="T0")
plt.plot(datetimes,temps1, label="T1")
plt.plot(datetimes,temps2, label="T2")
plt.plot(datetimes,temps3, label="T3")
plt.plot(datetimes,temps4, label="T4")
plt.plot(datetimes,temps5, label="T5")
plt.legend()

plt.gcf().autofmt_xdate()

plt.savefig(plot_file)

