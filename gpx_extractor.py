import gpxpy
import csv

##########
# gpx_extractor.py 
#  
# Accepts as input a  local .gpx file and converts the list of coordinates and timestamps 
# to a .csv file.  The .csv file can then be analyzed separately.
#
#
#
#
# Last Update: May 26, 2014
# Status: Working
##########


# Setup Input/Output file paths
output = open("GPX_Data.csv","w")
gpx_file = open('/home/cdurney/Documents/Running/Data/Python_Attempt/GPX Files May_22/20120921-111838-Run.gpx','r')


# Parsing an existing file:
gpx = gpxpy.parse(gpx_file)

# get a csv writer
writer = csv.writer( output )
writer.writerow(["Latitude", "Longitude", "Elevation", "TimeStamp"])	# Write a header row

#####
# Code for printing relevant information from .gpx file to a CSV file
for track in gpx.tracks:
	for segment in track.segments:
		for point in segment.points:
			data = [(point.latitude, point.longitude, point.elevation,point.time)]
			[ writer.writerow(x) for x in data ]
	print "Track in gpx.tracks ran"

for waypoint in gpx.waypoints:
	data = [(waypoint.name, waypoint.latitude, waypoint.longitude,waypoint.time)]
	[ writer.writerow(x) for x in data ]
	print "Waypoint in gpx.waypoints ran"

for route in gpx.routes:
	output.write('Route:')
	for point in route.points:
		data[(point.latitude, point.longitude, point.elevation,point.time)]
		[ writer.writerow(x) for x in data ]
	print "Route in gpx.routes ran"

gpx_file.close()
output.close()

