import datetime
import numpy as np
import matplotlib.pyplot as plt 
from numpy import loadtxt

# input output processing 
txt_file = "output/2019-12-13_12:02:22.txt"
plot_file = "plots/{}.pdf".format(txt_file.split("/")[1])


# load text 
datetimes = []
resists   = []
temps     = []
for line in open(txt_file,"r").readlines():

    # get infos
    date   = line.split()[0]
    time   = line.split()[1]
    resist = float(line.split()[2])
    temp   = float(line.split()[3])

    # format datetime obj
    datetime_str = "{} {}".format(date,time)
    datetime_obj = datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S.%f')

    # append
    datetimes.append(datetime_obj)
    resists.append(resist)
    temps.append(temp)

    # debug
    print(datetime_obj, temp)
 

# plot
plt.xlabel("Time") 
plt.ylabel("Temp [C]") 
plt.plot(datetimes,temps)
plt.gcf().autofmt_xdate()
#plt.show()


plt.savefig(plot_file)

