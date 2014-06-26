import csv
import sys
import numpy as np
import pylab as pl
import matplotlib.dates 

##########
# tcx_analyzer.py 
#  
# Accepts as input a .csv file formatted at function call
# Example: python tcx_analyzer Sample.tcx
# 
#
# Last Update: June 26, 2014
# Status:  Working
#   
# 
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

def smoothTriangle(data,degree,dropVals=False):
#performs moving triangle smoothing with a variable degree.
#note that if dropVals is False, output length will be identical
#to input length, but with copies of data at the flanking regions
    triangle=np.array(range(degree)+[degree]+range(degree)[::-1])+1
    smoothed=[]
    for i in range(degree,len(data)-degree*2):
        point=data[i:i+len(triangle)]*triangle
        smoothed.append(sum(point)/sum(triangle))
    if dropVals: return smoothed
    smoothed=[smoothed[0]]*(degree+degree/2)+smoothed
    while len(smoothed)<len(data):smoothed.append(smoothed[-1])
    return smoothed

with open(sys.argv[1],'rb') as f:
    data = np.genfromtxt(f, delimiter=',', names=True)
   
# Elevation vs. Distance 
    if raw_input('Plot Elevation vs. Distance: ').lower() == ('y' or 'yes'):
        fig = pl.figure()
        ax1 = fig.add_subplot(111)
        ax1.plot(data['Distance'], data['Altitude'], color='r')
        pl.xlabel("Distance (mi)") 
        pl.ylabel("Elevation (ft.)")
        pl.xlim([0,data['Distance'][-1]])
        pl.ylim([0,1500])

# Elevation vs. Time
    if raw_input('Plot Elevation vs. Time: ').lower() == ('y' or 'yes'):
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
    if raw_input('Plot Distance vs. Time: ').lower() == ('y' or 'yes'):
        fig = pl.figure()
        ax3 = fig.add_subplot(111)
        ax3.plot(data['ElapsedTime'], data['Distance'], color='r')
        ax3 = pl.gca()
        ax3.xaxis.set_major_formatter(pl.FuncFormatter(HMS)) 

        pl.xlabel("Time") 
        pl.ylabel("Distance (mi)")
        pl.xlim([0,data['ElapsedTime'][-1]])

# Pace vs. Time
    if raw_input('Plot Pace vs. Time: ').lower() == ('y' or 'yes'):
        fig = pl.figure()
        ax4 = fig.add_subplot(111)
        ax4.plot(data['ElapsedTime'], data['Pace'], color='b')
        ax4 = pl.gca()
        ax4.xaxis.set_major_formatter(pl.FuncFormatter(HMS)) 
        ax4.yaxis.set_major_formatter(pl.FuncFormatter(HMS))
        pl.xlabel("Time") 
        pl.ylabel("Pace")
        pl.xlim([0,data['ElapsedTime'][-1]])
        pl.ylim([240,720])

### GRAPH ORIGINAL/SMOOTHED DATA ###
#        fig = pl.figure()
#        pl.title("Moving Triangle Smoothing")
#        ax5 = fig.add_subplot(111)
        pl.plot(data['ElapsedTime'],smoothTriangle(data['Pace'],10),label="smoothed d=10",color='r')
#        ax5 = pl.gca()
#        ax5.xaxis.set_major_formatter(pl.FuncFormatter(HMS)) 
#        ax5.yaxis.set_major_formatter(pl.FuncFormatter(HMS))
#        pl.xlabel("Time") 
#        pl.ylabel("Pace")
#        pl.xlim([0,data['ElapsedTime'][-1]])
#        pl.ylim([240,720])
        pl.legend()

file = open(sys.argv[1],'rb')
reader = csv.reader(file)
header = reader.next()
if 'Pulse' in header:
    file.close() 
    with open(sys.argv[1],'rb') as f:
        if raw_input('Plot Pulse vs. Time: ').lower() == ('y' or 'yes'):
            data = np.genfromtxt(f, delimiter=',', names=True)
        # Heart Rate vs. Time
            fig = pl.figure()
            ax6 = fig.add_subplot(111)
            ax6.plot(data['ElapsedTime'], data['Pulse'], color='r')
            ax6 = pl.gca()
            ax6.xaxis.set_major_formatter(pl.FuncFormatter(HMS)) 
            pl.xlabel("Time") 
            pl.ylabel("Heart Rate")
            pl.xlim([0,data['ElapsedTime'][-1]])
            pl.ylim([40,190])
        
        if raw_input('Scatter Plot Pulse vs. Pace: ').lower() == ('y' or 'yes'):
            fig = pl.figure()
            ax7 = fig.add_subplot(111)
            ax7.scatter(data['Pace'],data['Pulse'],color='blue',s=5,edgecolor='none')
            ax7.xaxis.set_major_formatter(pl.FuncFormatter(HMS)) 
            #ax7.set_aspect(1./ax7.get_data_ratio()) # make axes square
            pl.xlabel("Pace") 
            pl.ylabel("Heart Rate")
            pl.ylim([40,190])


pl.show()







