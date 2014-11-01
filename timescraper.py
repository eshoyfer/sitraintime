# -*- coding: utf-8 -*-

import collections
import pickle
import datetime

# Indices

# To St George 
# 1. Tville ....... 21. St. George

station_formatted_names = {'tottenville': 'Tottenville', 'atlantic': 'Atlantic', 'nassau': 'Nassau', 'richmond_valley': 'Richmond Valley', 
						'pleasant_plains': 'Pleasant Plains', 'princes_bay': "Prince's Bay", 'huguenot': 'Huguenot', 'annadale': 'Annadale',
						'eltingville': 'Eltingville', 'great_kills': 'Great Kills', 'bay_terrace': 'Bay Terrace', 'oakwood_heights': 'Oakwood Heights',
						'new_dorp': 'New Dorp', 'grant_city': 'Grant City', 'jefferson_av': 'Jefferson Av', 'dongan_hills': 'Dongan Hills', 
						'old_town': 'Old Town', 'grasmere': 'Grasmere', 'clifton': 'Clifton', 'stapleton': 'Stapleton', 'tompkinsville': 'Tompkinsville',
						'st_george': 'St George'
						}

to_st_george_list = ['tottenville', 'atlantic', 'nassau', 'richmond_valley', 'pleasant_plains', 'princes_bay', 'huguenot', 'annadale',
					'eltingville', 'great_kills', 'bay_terrace', 'oakwood_heights', 'new_dorp', 'grant_city', 'jefferson_av',
					'dongan_hills', 'old_town', 'grasmere', 'clifton', 'stapleton', 'tompkinsville', 'st_george'
					]

to_tottenville_list = to_st_george_list[::-1]

# AM/PM <-> 24 hour stuff

def convert_pm_to_24(s):
	hours_mins = s.split(':')

	hours_string = hours_mins[0]
	mins_string = hours_mins[1]

	hours_string = str((int(hours_string) % 12) + 12)

	converted = hours_string + ":" + mins_string
	return converted

def convert_am_to_24(s):
	hours_mins = s.split(':')

	hours_string = hours_mins[0]
	mins_string = hours_mins[1]

	hours_string = str(int(hours_string) % 12)

	converted = hours_string + ":" + mins_string
	return converted

def convert_to_24(s):
	
	if s != "skip":
		time_type = s[-1]
		if (time_type == "a"):
			converted = convert_am_to_24(s[:-1])
		elif (time_type == "p"):
			converted = convert_pm_to_24(s[:-1])
	else:
		converted = "skip"

	return converted

def mark_am(s):
	if (s == "—"):
		return "skip"

	return s + 'a'

def mark_pm(s):
	if (s == "—"):
		return "skip"

	return s + 'p'

def strip_mark(s):
	return s[:-1]

def convert_to_time_object(s):
	if s != "skip":
		hours_mins = s.split(':')
		hours = int(hours_mins[0])
		mins = int(hours_mins[1])
		return datetime.time(hours, mins, 0, 0)
	else:
		return "skip"


# Preparing dictionary for data

# Example of layout:

# Schedules

# new_dorp_dictionary = data['schedules']['weekday']['st_george']['new_dorp']
# new_dorp_dictionary[time] = [type, route]

# Time is a 24-hour time, e.g. 12:51
# Type is A, B, C, D, E, F
# Route is route/row ID for lookup in route dictionary

# Routes

# route_dictionary = data['routes']
# route_dictionary[ID] = [type, stops_array]

# Route is route ID 
# stops_array is a list of times for stops, e.g. [11:52, 12:07, 12:22]
# Type is A, B, C, D, E, F

# Ferry times will be a seperate thing later

# Raw data info:

# Always 24 columns

# Weekday_St_George: 67
# Weekday_Tottenville: 74
# Saturday_St_George: 45
# Saturday_Tottenville: 45
# Sunday_St_George: 45 
# Sunday_Tottenville: 45 

# To St George: 2 ferry columns on right
# To Tottenville: 2 ferry columns on left


data = {
	'schedules': {
		'weekday': {
			'st_george': {},
			'tottenville': {}
		},

		'saturday': {
			'st_george': {},
			'tottenville': {}
		},

		'sunday': {
			'st_george': {},
			'tottenville': {}
		}
	},

	'routes': {

	}
}

for schedule_type in data['schedules']:
	for direction in data['schedules'][schedule_type]:
		for station in to_st_george_list:
			data['schedules'][schedule_type][direction][station] = collections.OrderedDict()


# Modifying raw data files from http://web.mta.info/nyct/service/pdf/sircur.pdf

# Data was copied.

# By hand:
# 1. "Ferry only" two column rows were removed
# 2. The first pm stop was marked with a single p and the first am stop after the pm stops (if any) was marked with a single a

def modify_raw_data(filename):
	f = open(filename, 'r')

	wsg_string = f.read()
	f.close()

	wsg_string_rows = wsg_string.splitlines()

	wsg_table = []

	for row in wsg_string_rows:
		row_list = row.split();
		wsg_table.append(row_list)

	markingAM = True

	new_table = []

	for i in range(len(wsg_table)):
		new_table.append(["empty" for i in range(22)])

	for i in range(len(wsg_table)):
		if "st_george" in filename:
			for j in range(22): # Remove ferry columns
				this_data = wsg_table[i][j]
				print this_data
				if 'p' in this_data: # Marked by hand where PM starts
					markingAM = False
				if 'a' in this_data: 
					markingAM = True
				if 'p' in this_data or 'a' in this_data:
					this_data = this_data[:-1]
				changed_data = ""
				if markingAM:
					changed_data = mark_am(this_data)
				else:
					changed_data = mark_pm(this_data)
				new_table[i][j] = changed_data
		else:
			ferryScheduleType = True
			try:
				probe = wsg_table[i][23]
				ferryScheduleType = True
				# If successful, fully filled, including ferry times.
			except:
				ferryScheduleType = False
				# If failure, it's not fully filled - only indices 0 to 21 are filled, no ferry times.
			if ferryScheduleType:
				for j in range(2,24): # Remove ferry columns
					
					this_data = wsg_table[i][j]
					
					if 'p' in this_data: # Marked by hand where PM starts
						markingAM = False
					if 'a' in this_data:
						markingAM = True
					if 'p' in this_data or 'a' in this_data:
						this_data = this_data[:-1]
					changed_data = ""
					if markingAM:
						changed_data = mark_am(this_data)
					else:
						changed_data = mark_pm(this_data)
					new_table[i][j-2] = changed_data
			else:
				for j in range(22): # Remove ferry columns
					
					this_data = wsg_table[i][j]
					
					if 'p' in this_data: # Marked by hand where PM starts
						markingAM = False
					if 'a' in this_data:
						markingAM = True
					if 'p' in this_data or 'a' in this_data:
						this_data = this_data[:-1]
					changed_data = ""
					if markingAM:
						changed_data = mark_am(this_data)
					else:
						changed_data = mark_pm(this_data)
					new_table[i][j] = changed_data

	replacement_text = ""
	for i in range(len(new_table)):
		for j in range(22):
			this_data = new_table[i][j]
			replacement_text += this_data + " "
		replacement_text = replacement_text[:-1] + "\n"
	replacement_text = replacement_text[:-1] # Get rid of the last \n

	f = open(filename, 'w')
	f.write(replacement_text)
	f.close()

# Modify all the data

# Run this once:

#modify_raw_data('weekday_st_george_raw.txt')
#modify_raw_data('weekday_tottenville_raw.txt')
#modify_raw_data('saturday_st_george_raw.txt')
#modify_raw_data('saturday_tottenville_raw.txt')
#modify_raw_data('sunday_st_george_raw.txt')
#modify_raw_data('sunday_tottenville_raw.txt')

# Scraping St. George Weekday

# Refactor into a generalized function

def retrieve_table_from_data(filename):

	f = open(filename, 'r')

	wsg_string = f.read()
	f.close()

	wsg_string_rows = wsg_string.splitlines()

	wsg_table = []

	for row in wsg_string_rows:
		row_list = row.split();
		wsg_table.append(row_list)

	# wsg_table is now a two-dimensional array 
	# First, access rows 
	# Then columns to get individual cells

	return wsg_table

def convert_table_to_24(t):
	for i in range(len(t)):
		for j in range(22):
			this_data = t[i][j]
			new_data = convert_to_time_object(convert_to_24(this_data)) 
			# To use 24H HH:MM instead of time objects, remove conversion wrapper function
			t[i][j] = new_data

	return t		

#global_route_number_count = 1

def determine_route_type(train_list, direction):
	# A: Regular. Bidirectional standard. No Skips. - True regular
	# B: Express. Skips after ND to SG. [TO ST GEORGE] - Morning to Manhattan express
 	# C: Regular that starts from GK, proceeds to SG. [TO ST GEORGE] - A regular that starts from Great Kills
	# D: Express. Skips to ND from SG. [TO TVILLE] - Evening return from Manhattan express, slower
	# E. Regular. Terminates at GK from SG. [TO TVILLE] - "Great Kills" train
	# F. Express. Skips to GK from SG. [TO TVILLE] - Evening return from Manhattan express, faster
	if "skip" not in train_list:
		return "A"

	elif direction == "st_george":
		if train_list[13] == "skip": # Grant City check 
			return "B"
		else:
			return "C"

	else:
		# Train list is in order of guide pull
		if train_list[10] != "skip": # Oakwood Heights check
			if train_list[8] == "skip": # Grant City Check [Note reversal from 13 of other Grant City check, 8 + 13 = 21]
				return "D"
			else:
				return "E"
		else:
			return "F"

def populate_dictionary(filename):
	table = convert_table_to_24(retrieve_table_from_data(filename))

	filename = filename.split('/')[-1]
	
	if "st_george" in filename:
		to_st_george = True
		direction = "st_george"
	else:
		to_st_george = False
		direction = "tottenville"

	schedule = filename.split('_')[0] # Reg, Sat, Sun
	# Schedule and direction for schedule type access


	routes_dictionary = data['routes']
	this_schedules_dictionary = data['schedules'][schedule][direction]

	for trainListNumber in range(len(table)):
		this_train_list = table[trainListNumber]
		route_type = determine_route_type(this_train_list, direction)
		# Route preservation in native orientation
		route_global_id = str(trainListNumber) + "_" + schedule + "_" + direction
		routes_dictionary[route_global_id] = [route_type, this_train_list]

		for stationIndex in range(22):
			this_stop_time = table[trainListNumber][stationIndex]

			if this_stop_time != "skip":
				if to_st_george:
					this_schedules_dictionary[to_st_george_list[stationIndex]][this_stop_time] = [route_type, route_global_id]
				else:
					this_schedules_dictionary[to_tottenville_list[stationIndex]][this_stop_time] = [route_type, route_global_id]

# Populating the dictionary

populate_dictionary('rawdata/weekday_st_george_raw.txt')
populate_dictionary('rawdata/weekday_tottenville_raw.txt')
populate_dictionary('rawdata/saturday_st_george_raw.txt')
populate_dictionary('rawdata/saturday_tottenville_raw.txt')
populate_dictionary('rawdata/sunday_st_george_raw.txt')
populate_dictionary('rawdata/sunday_tottenville_raw.txt')


# Produce times sorted in stop's proper order

def to_minutes(s):
	hours_mins = s.split(':')
	return int(hours_mins[0]) * 60 + int(hours_mins[1])

# station_dict example: data['schedules']['saturday']['tottenville']['princes_bay']
def station_stops(station_dict):

	#properly_sorted_times = sorted(station_dict.keys(), key=to_minutes)

	times = station_dict.keys()

	# Some stations will have a stop after midnight on the end of that day's cycle
	# which with a simple sort will get classified as coming before the actual first, post-midnight stop at the beginning of the cycle.
	# This was solved by using an OrderedDict initially, and removed the need for sorting the times at all. 
	# Data was inserted row by row, which preserved the proper order of times through the cycle.

	return times

#print station_stops(data['schedules']['saturday']['tottenville']['princes_bay'])
#print station_stops(data['schedules']['weekday']['st_george']['princes_bay'])
#print data['routes']

# Storing the data:
# Dictionary stored with pickle

data_file = open('traintimes.p', 'wb')
pickle.dump(data, data_file)
data_file.close()
