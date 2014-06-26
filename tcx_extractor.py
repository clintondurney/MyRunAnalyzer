import csv
import sys
from lxml import objectify, etree
import datetime 
import time
import numpy as np

##########
# tcx_extractor.py 
#  
# Accepts as input a .tcx file and converts extracts the desired
# fields of interest to be analyzed later.  Ouput is a csv file.
# 
#
# Last Update: June 25, 2014
# Status:  Added Pace to csv output 
# Goals: 
#        add cadence to csv output
# 
##########

def meters_to_feet(meters):
    return np.round(meters*3.2808399,4)

def meters_to_miles(meters):
    return np.round(meters*0.000621371,4)

def hms_to_seconds(time):
    h, m, s = [int(i) for i in time.split(':')]
    return 3600*h + 60*m + s

def Pace(t_1,t_2,d_1,d_2):
# Returns the (awkward) pace of seconds per mile
# which is useful later.
    if (d_2-d_1) == 0 or (t_2-t_1)/((d_2-d_1)) > 720:
        return 720
    else:
        return (t_2-t_1)/((d_2-d_1)) 



#############################################
# Works to give Lap, ElapsedTime, Distance, Altitude, Lat, Long
# The go to function if something stops working.
# 5/29/14
def Legacy(activity, start_time):
    for lap_counter,lap in enumerate(activity.Lap, start=1):
    # print lap_counter, lap.TotalTimeSeconds.pyval, lap.DistanceMeters.pyval
        for trackpoint in lap.Track.Trackpoint:
            if hasattr(trackpoint, 'DistanceMeters') == True and hasattr(trackpoint, 'Position'): 
                next_time = time.mktime(datetime.datetime.strptime(trackpoint.Time.pyval[11:-5], "%H:%M:%S").timetuple())        
                writer.writerow((lap_counter, hms_to_seconds(str(datetime.timedelta(seconds = next_time - start_time))), 
                meters_to_miles(trackpoint.DistanceMeters.pyval),
                meters_to_feet(trackpoint.AltitudeMeters.pyval), trackpoint.Position.LatitudeDegrees.pyval,
                trackpoint.Position.LongitudeDegrees.pyval))
#############################################

def Working(activity, start_time):
    for lap_counter,lap in enumerate(activity.Lap, start=1):
        print lap_counter, lap.TotalTimeSeconds.pyval, meters_to_miles(lap.DistanceMeters.pyval)
        data_old = [0,0,0,0,0,0,0]
        for trackpoint in lap.Track.Trackpoint:
            data = [lap_counter]
	    if hasattr(trackpoint, 'DistanceMeters') == True:
                next_time = time.mktime(datetime.datetime.strptime(trackpoint.Time.pyval[11:-5], "%H:%M:%S").timetuple())
	        data.append(hms_to_seconds(str(datetime.timedelta(seconds = next_time - start_time))))
                data.append(meters_to_miles(trackpoint.DistanceMeters.pyval))
                data.append(Pace(data_old[1],data[1],data_old[2],data[2]))
		data.append(meters_to_feet(trackpoint.AltitudeMeters.pyval))
		data.append(trackpoint.Position.LatitudeDegrees.pyval)
		data.append(trackpoint.Position.LongitudeDegrees.pyval)
		data.append(int(1))
                data_old = data
		writer.writerow(data)

def WorkingPulse(activity, start_time):
    for lap_counter,lap in enumerate(activity.Lap, start=1):
        print lap_counter, lap.TotalTimeSeconds.pyval, meters_to_miles(lap.DistanceMeters.pyval)
        data_old = [0,0,0,0,0,0,0]
        for trackpoint in lap.Track.Trackpoint:
            data = [lap_counter]
	    if hasattr(trackpoint, 'DistanceMeters') == True:
                next_time = time.mktime(datetime.datetime.strptime(trackpoint.Time.pyval[11:-5], "%H:%M:%S").timetuple())
	        data.append(hms_to_seconds(str(datetime.timedelta(seconds = next_time - start_time))))
                data.append(meters_to_miles(trackpoint.DistanceMeters.pyval))
                data.append(Pace(data_old[1],data[1],data_old[2],data[2]))
		data.append(meters_to_feet(trackpoint.AltitudeMeters.pyval))
		data.append(trackpoint.Position.LatitudeDegrees.pyval)
		data.append(trackpoint.Position.LongitudeDegrees.pyval)
	        if hasattr(trackpoint,'HeartRateBpm') == True:
                    data.append(trackpoint.HeartRateBpm.Value.pyval)
                else:
                    data.append(int(0))
                data_old = data
		writer.writerow(data)
#######################################

###########
#
############
with open(sys.argv[1],'r') as f:
    with open(sys.argv[2], "w") as o:
        # get a csv writer
        writer = csv.writer(o)
        # write the header file
        # writer.writerow(("Lap", "ElapsedTime", "Distance", "Pace", "Altitude", "Latitude", "Longitude"))
        tree = objectify.parse(f)
        root = tree.getroot()
        activity = root.Activities.Activity
        s = activity.Lap.Track.Trackpoint.Time.pyval
        start_time = time.mktime(datetime.datetime.strptime(s[11:-5], "%H:%M:%S").timetuple())
        
        if hasattr(activity.Lap,'AverageHeartRateBpm') == True:
            writer.writerow(("Lap", "ElapsedTime", "Distance", "Pace", "Altitude", "Latitude", "Longitude","Pulse"))
            WorkingPulse(activity, start_time)
        else:
            writer.writerow(("Lap", "ElapsedTime", "Distance", "Pace", "Altitude", "Latitude", "Longitude","Pulse"))
            Working(activity, start_time)



