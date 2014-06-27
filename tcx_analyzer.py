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

def Elevation_vs_Distance(data):
    fig = pl.figure()
    ax1 = fig.add_subplot(111)
    ax1.plot(data['Distance'], data['Altitude'], color='r')
    pl.xlabel("Distance (mi)") 
    pl.ylabel("Elevation (ft.)")
    pl.xlim([0,data['Distance'][-1]])
    pl.ylim([0,1500])

def Elevation_vs_Time(data):        
    fig = pl.figure()
    ax2 = fig.add_subplot(111)
    ax2.plot(data['MovingTime'], data['Altitude'], color='r')
    ax2 = pl.gca()
    ax2.xaxis.set_major_formatter(pl.FuncFormatter(HMS)) 
    pl.xlabel("Time") 
    pl.ylabel("Elevation (ft.)")
    pl.xlim([0,data['MovingTime'][-1]])
    pl.ylim([0,1500])

def Distance_vs_Time(data):
    fig = pl.figure()
    ax3 = fig.add_subplot(111)
    ax3.plot(data['MovingTime'], data['Distance'], color='r')
    ax3 = pl.gca()
    ax3.xaxis.set_major_formatter(pl.FuncFormatter(HMS)) 
    pl.xlabel("Time") 
    pl.ylabel("Distance (mi)")
    pl.xlim([0,data['MovingTime'][-1]])

def Pace_vs_Time(data):
    fig = pl.figure()
    ax4 = fig.add_subplot(111)
    ax4.plot(data['MovingTime'], data['Pace'], color='b')
    ax4 = pl.gca()
    ax4.xaxis.set_major_formatter(pl.FuncFormatter(HMS)) 
    ax4.yaxis.set_major_formatter(pl.FuncFormatter(HMS))
    pl.xlabel("Time") 
    pl.ylabel("Pace")
    pl.xlim([0,data['MovingTime'][-1]])
    pl.ylim([240,720])

### GRAPH ORIGINAL/SMOOTHED DATA ###
#    fig = pl.figure()
#    pl.title("Moving Triangle Smoothing")
#    ax5 = fig.add_subplot(111)
    pl.plot(data['MovingTime'],smoothTriangle(data['Pace'],10),label="smoothed d=10",color='r')
#    ax5 = pl.gca()
#    ax5.xaxis.set_major_formatter(pl.FuncFormatter(HMS)) 
#    ax5.yaxis.set_major_formatter(pl.FuncFormatter(HMS))
#    pl.xlabel("Time") 
#    pl.ylabel("Pace")
#    pl.xlim([0,data['ElapsedTime'][-1]])
#    pl.ylim([240,720])
    pl.legend()

def Pace_Dist(data):
    fig = pl.figure()
    ax9 = fig.add_subplot(111)
    num_bins = 50
    ax9.hist(data['Pace'],num_bins)
    ax9.xaxis.set_major_formatter(pl.FuncFormatter(HMS))
    pl.xlabel("Pace")

def HR_vs_Time(data):
    fig = pl.figure()
    ax6 = fig.add_subplot(111)
    ax6.plot(data['MovingTime'], data['Pulse'], color='r')
    ax6 = pl.gca()
    ax6.xaxis.set_major_formatter(pl.FuncFormatter(HMS)) 
    pl.xlabel("Time") 
    pl.ylabel("Heart Rate")
    pl.xlim([0,data['MovingTime'][-1]])
    pl.ylim([40,190])
        
def HR_Pace(data):
    fig = pl.figure()
    ax7 = fig.add_subplot(111)
    ax7.scatter(data['Pace'],data['Pulse'],color='blue',s=5,edgecolor='none')
    ax7.xaxis.set_major_formatter(pl.FuncFormatter(HMS)) 
    #ax7.set_aspect(1./ax7.get_data_ratio()) # make axes square
    pl.xlabel("Pace") 
    pl.ylabel("Heart Rate")
    pl.ylim([40,190])

def Pulse_Dist(data):
    fig = pl.figure()
    ax8 = fig.add_subplot(111)
    num_bins = 50 
    ax8.hist(np.trim_zeros(data['Pulse']),num_bins)
    pl.xlabel("Pulse")
    pl.xlim([40,190])
    pl.title("Distribution of Pulse")

with open(sys.argv[1],'rb') as f:
    data = np.genfromtxt(f, delimiter=',', names=True)
   
# Calculate certain metrics with file open and save for later use
    total_time = data['ElapsedTime'][-1]
    moving_time = data['MovingTime'][-1]
    total_distance = data['Distance'][-1]
    avg_pace = np.mean(data['Pace'])
    max_hr = max(data['Pulse'])
    min_hr = np.min(data['Pulse'][np.nonzero(data['Pulse'])])
    avg_hr = np.mean(data['Pulse'][np.nonzero(data['Pulse'])])

    if raw_input('Plot Elevation vs. Distance: ').lower() == ('y' or 'yes'):
	Elevation_vs_Distance(data)
    if raw_input('Plot Elevation vs. Time: ').lower() == ('y' or 'yes'):
	Elevation_vs_Time(data)
    if raw_input('Plot Distance vs. Time: ').lower() == ('y' or 'yes'):
 	Distance_vs_Time(data)       
    if raw_input('Plot Pace vs. Time: ').lower() == ('y' or 'yes'):
	Pace_vs_Time(data)
    if raw_input('Pace Distribution: ').lower() == ('y' or 'yes'):
        Pace_Dist(data)
    if int(max_hr) != int(1):
    	if raw_input('Plot Pulse vs. Time: ').lower() == ('y' or 'yes'):
 	    HR_vs_Time(data)       
        if raw_input('Scatter Plot Pulse vs. Pace: ').lower() == ('y' or 'yes'):
	    HR_Pace(data)
        if raw_input('Pulse Distribution: ').lower() == ('y' or 'yes'):
            Pulse_Dist(data)

print "Total Distance = ", total_distance, " miles"
print "Total Time = ", HMS(total_time,1)
print "Moving Time = ", HMS(moving_time,1)
print "Average Pace = ", HMS(avg_pace,1)
if int(max_hr) == 1:
    print "Minimum Heart Rate = -"
    print "Maximum Heart Rate = -"
    print "Average Heart Rate = -"
else:
    print "Minimum Heart Rate = ", int(min_hr)
    print "Maximum Heart Rate = ", int(max_hr)
    print "Average Heart Rate = ", int(round(avg_hr))

pl.show()


