import datetime
import numpy as np
import matplotlib.pyplot as plt 
from numpy import loadtxt

# input output processing 
txt_file = "output/2019-12-16_11:36:53.txt"
plot_file = "plots/{}.pdf".format(txt_file.split("/")[1])


# load text 
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
 

# plot
plt.xlabel("Time") 
plt.ylabel("Temp [C]") 
plt.plot(datetimes,temps0, label="T0")
plt.plot(datetimes,temps1, label="T1")
plt.plot(datetimes,temps2, label="T2")
plt.plot(datetimes,temps3, label="T3")
plt.plot(datetimes,temps4, label="T4")
plt.plot(datetimes,temps5, label="T5")
plt.legend()
#plt.legend( (T0, T1, T2, T3, T4, T5),("T0","T1","T2","T3","T4","T5"))

plt.gcf().autofmt_xdate()
#plt.show()


plt.savefig(plot_file)

