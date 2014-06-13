import csv
import numpy as np
import pylab as pl
import matplotlib.dates 

##########
# tcx_analyzer.py 
#  
# Accepts as input a .csv file formatted as 
#
# 
#
# Last Update: June 13, 2014
# Status:  None
#   Goals:
#   1. 
##########

def HMS(seconds, pos):
    seconds = int(seconds)
    hours = seconds / 3600
    seconds -= 3600 * hours
    minutes = seconds / 60
    seconds -= 60 * minutes
    if hours == 0:
        return "%02d:%02d" % (minutes,seconds)
    else: 
        return "%d:%02d:%02d" % (hours, minutes,seconds)


with open("Sample2.csv",'rb') as f:
    data = np.genfromtxt(f, delimiter=',', names=True)
   
# Elevation vs. Distance 
    fig = pl.figure()
    ax1 = fig.add_subplot(111)
    ax1.plot(data['Distance'], data['Altitude'], color='r')
    pl.xlabel("Distance (mi)") 
    pl.ylabel("Elevation (ft.)")
    pl.xlim([0,data['Distance'][-1]])
    pl.ylim([0,1500])

# Elevation vs. Time
    fig = pl.figure()
    ax2 = fig.add_subplot(111)
    ax2.plot(data['ElapsedTime'], data['Altitude'], color='r')
    ax2 = pl.gca()
    ax2.xaxis.set_major_formatter(pl.FuncFormatter(HMS)) 

    pl.xlabel("Time") 
    pl.ylabel("Elevation (ft.)")
    pl.xlim([0,data['ElapsedTime'][-1]])
    pl.ylim([0,1500])

# Distance vs. Time
    fig = pl.figure()
    ax3 = fig.add_subplot(111)
    ax3.plot(data['ElapsedTime'], data['Distance'], color='r')
    ax3 = pl.gca()
    ax3.xaxis.set_major_formatter(pl.FuncFormatter(HMS)) 

    pl.xlabel("Time") 
    pl.ylabel("Distance (mi)")
    pl.xlim([0,data['ElapsedTime'][-1]])

# Pace vs. Time
    fig = pl.figure()
    ax4 = fig.add_subplot(111)
    ax4.plot(data['ElapsedTime'], data['Pace'], color='r')
    ax4 = pl.gca()
    ax4.xaxis.set_major_formatter(pl.FuncFormatter(HMS)) 
    ax4.yaxis.set_major_formatter(pl.FuncFormatter(HMS))
    pl.xlabel("Time") 
    pl.ylabel("Pace")
    pl.xlim([0,data['ElapsedTime'][-1]])
    pl.ylim([240,600])
pl.show()
   








