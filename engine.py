import pickle
import datetime
import calendar
import time
import math
import timescraper

#####################################################################################

### Data Loading ###

data_file = open('traintimes.p', 'rb')
data = pickle.load(data_file)
data_file.close()

#####################################################################################

### Schedule Determination ###

# Holidays: 
# Martin Luther King Day, Columbus Day, Veterans Day, Election Day, the Day after Thanksgiving --> Weekday Schedule 
# No Detection Needed

# New Years Day, Presdients Day, Memorial Day, Independence Day, Labor Day, Thanksgiving Day, Christmas Day:
# On Tuesday through Friday --> Saturday Schedule
# On Saturday, Sunday, Monday --> Sunday Schedule 

# Given date object: will be today's date in implementation

# Returns a date object representing the nth weekday (given type) of a given month from a given year
def nth_weekday(month, year, n, weekday):
	counter = 0
	for day in calendar.Calendar().itermonthdates(year, month):
		if day.month == month and day.weekday() == weekday:
			counter += 1
			if counter == n:
				return day

# Returns the number of given weekday in a specified month (How many Mondays are in July 2014?)
# Monday = 0, Sunday = 6
def number_of_weekdays(month, year, weekday):
	counter = 0
	for day in calendar.Calendar().itermonthdates(year, month):
		if day.month == month and day.weekday() == weekday:
			counter += 1
	return counter


## Holiday Checks ##

# January 1
def get_new_years_day(given_date):
	year = given_date.year
	return datetime.date(year, 1, 1)

def is_new_years_day(given_date):
	holiday = get_new_years_day(given_date)
	return holiday == given_date

# Third Monday in February
def get_presidents_day(given_date):
	year = given_date.year
	return nth_weekday(2, year, 3, 0)

def is_presidents_day(given_date):
	holiday = get_presidents_day(given_date)
	return holiday == given_date

# Last Monday in May
def get_memorial_day(given_date):
	year = given_date.year
	mondays = number_of_weekdays(5, year, 0)
	return nth_weekday(5, year, mondays, 0)

def is_memorial_day(given_date):
	holiday = get_memorial_day(given_date)
	return holiday == given_date	

# 4th of July
def get_independence_day(given_date):
	year = given_date.year
	return datetime.date(year, 7, 4)

def is_independence_day(given_date):
	holiday = get_independence_day(given_date)
	return holiday == given_date

# First Monday in September
def get_labor_day(given_date):
	year = given_date.year
	return nth_weekday(9, year, 1, 0)

def is_labor_day(given_date):
	holiday = get_labor_day(given_date)
	return holiday == given_date

# Fourth Thursday of November
def get_thanksgiving(given_date):
	year = given_date.year
	return nth_weekday(11, year, 4, 3)

def is_thanksgiving(given_date):
	holiday = get_thanksgiving(given_date)
	return holiday == given_date

# Christmas: December 25th
def get_christmas(given_date):
	year = given_date.year
	return datetime.date(year, 12, 25)

def is_christmas(given_date):
	holiday = get_christmas(given_date)
	return holiday == given_date

## Combined check ##
def is_holiday(given_date):
	return (
			is_new_years_day(given_date) or is_presidents_day(given_date) or
			is_memorial_day(given_date) or is_independence_day(given_date) or
			is_labor_day(given_date) or is_thanksgiving(given_date) or
			is_christmas(given_date)
		)

## Schedule determination

def determine_schedule_type(given_date):
	weekday = given_date.weekday() # Monday is 0, Sunday is 6

	if is_holiday(given_date):
		if (weekday >= 1 and weekday <= 4): # Tuesday through Friday
			return "saturday"
		else:
			return "sunday"
	else:
		if (weekday <= 4): # Monday through Friday
			return "weekday"
		elif (weekday == 5):
			return "saturday"
		else:
			return "sunday" 


def today_schedule_type():
	return determine_schedule_type(datetime.date.today())

## Assorted Tests

#print data
#print data['routes']
# for i in range(1,6):
# 	print nth_weekday(2, 2014, i, 4), "hey"
# for i in range(7):
# 	print number_of_weekdays(2, 2014, i)
#start = time.time()
#for j in range(1,13):
#	for i in range(1,28):
#		print is_holiday(datetime.date(2014, j, i)), datetime.date(2014, j, i)
#end = time.time()
#print float(end-start)
# for month in range(1,13):
# 	for date in range(1, 32):
# 		try:
# 			print datetime.date(2014, month, date), is_holiday(datetime.date(2014, month, date))
# 		except:
# 			print "no date"

#print today_schedule_type() # Today
#print determine_schedule_type(datetime.date(2014, 7, 12)) # Regular Saturday
#print determine_schedule_type(datetime.date(2014, 7, 13)) # Regular Sunday
#print determine_schedule_type(datetime.date(2014, 7, 4)) # 4th of July, a holiday on a Friday, triggering a Saturday schedule
#print determine_schedule_type(datetime.date(2014, 9, 1)) # Labor Day, a holiday on a Monday, triggering a Sunday schedule

#####################################################################################

### Train Times ###

# Train times: Given a station and direction, get the next train that's coming. 

# A list of a given station's stops, given the dictionary with the times selected. 
data['schedules']['saturday']['tottenville']['princes_bay']


def format_stop(stop_id):
	return timescraper.station_formatted_names[stop_id]

def get_station_dict(schedule, direction, station):
	return data['schedules'][schedule][direction][station]

def station_stops(schedule, direction, station):
	times = get_station_dict(schedule, direction, station).keys()
	return times

def get_train_type(schedule, direction, station, time):
	times_dict = get_station_dict(schedule, direction, station)
	return times_dict[time][0]

def get_train_id(schedule, direction, station, time):
	times_dict = get_station_dict(schedule, direction, station)
	return times_dict[time][1] 

# Takes a sorted list of train times (sorted in order) and returns x's relative position in the list.
# x is a time. sortedL is a list of times.
def get_relative_position(sortedL, x):
	# Counter is a representation of relative position in a sorted list.
	# The value of the counter is equal to the number of hops within the time stop list needed to get between the two times. 
	# Example:
	# A list, [1, 2, 3, 4]
	# A counter of 0 --> It's before 1. 
	# A counter of 1 --> Between 1 and 2. 
	# A counter of 2 --> Between 2 and 3. 
	# A counter of 3 --> Between 3 and 4. 
	# A counter of 4 --> After 4. 

	# If counter is 0 --> Smaller than everything 
	# If counter is equal to len(list) --> Greater than everything

	counter = 0 

	# Can be made faster with a binary search but should do
	for i in sortedL:
		if x >= i:
			counter += 1
	if sortedL[-1] < sortedL[-2]:
		counter -= 1 # Account for the midnight wrap around case 		
	return counter
	
def format_time(datetime):
	format = "%I:%M %p"
	if datetime != "skip":
		date_time_formatted = datetime.strftime(format)
	else:
		date_time_formatted = "--"
	return date_time_formatted

# Date_time is a datetime object; this version returns date_time objects

## Next and prev time functions

## Note: All of these functions return a tuple of the form (datetime_object_of_stoptime, train_type, train_id)
def prev_time_params(direction, station, date_time):
	schedule = determine_schedule_type(date_time)
	times = station_stops(schedule, direction, station)
	time_now = datetime.datetime.time(date_time)
	position = get_relative_position(times, time_now)
	number_behind = position
	number_front = len(times) - position
	if number_behind > 0:
		prev_time = times[position - 1] 
		# If this is a midnight wraparound case, increment the datetime object's date
		if (position == (len(times) - 1)) and (prev_time.hour == 0):
			used_date_time = date_time + timedelta(days = 1)
		else:
			used_date_time = date_time
		prev_time_date = datetime.datetime(used_date_time.year, used_date_time.month, used_date_time.day, prev_time.hour, prev_time.minute, prev_time.second,
						prev_time.microsecond)
		# Schedule, direction, station, time
		train_type = get_train_type(schedule, direction, station, prev_time)
		train_id = get_train_id(schedule, direction, station, prev_time)
		return prev_time_date, train_type, train_id
	else:
		# Get the last time of yesterday's schedule.
		# Recursive solution (as in next_time) doesn't work because the latest "yesterday" datetime is 23:59:59:9999, and would not account for the midnight
		# wraparound cases. 
		# Trying to hardcode based on relative position would interfere with legitimate cases.
		yesterday = date_time - datetime.timedelta(days = 1)
		yesterday_schedule = determine_schedule_type(yesterday)
		times_yesterday = station_stops(yesterday_schedule, direction, station)
		new_position = get_relative_position(times_yesterday, time_now)
		last_time_yesterday = times_yesterday[new_position - 1]
		if last_time_yesterday.hour == 0: # After midnight stop included in yesterday's schedule (wraparound case), increment date
			used_date_time = yesterday + datetime.timedelta(days = 1) # This is just date_time, but arithmetic shown for clarity
		else: # Part of yesterday's date and in yesterday's schedule
			used_date_time = yesterday

		last_time_yesterday_date = datetime.datetime(used_date_time.year, used_date_time.month, used_date_time.day,
									last_time_yesterday.hour, last_time_yesterday.minute, last_time_yesterday.second, last_time_yesterday.microsecond)
		train_type = get_train_type(yesterday_schedule, direction, station, last_time_yesterday)
		train_id = get_train_id(yesterday_schedule, direction, station, last_time_yesterday)
		return last_time_yesterday_date, train_type, train_id


def next_time_params(direction, station, date_time):
	schedule = determine_schedule_type(date_time)
	times = station_stops(schedule, direction, station)
	time_now = datetime.datetime.time(date_time)
	position = get_relative_position(times, time_now)
	number_behind = position
	number_front = len(times) - position
	if number_front > 0:
		next_time = times[position]
		if (position == (len(times) - 1)) and (next_time.hour == 0): # If this is a midnight wraparound case, increment the datetime object's date
			used_date_time = date_time + datetime.timedelta(days = 1)
		else:
			used_date_time = date_time 
		next_time_date = datetime.datetime(used_date_time.year, used_date_time.month, used_date_time.day, next_time.hour, next_time.minute, next_time.second,
							next_time.microsecond)
		time_difference = next_time_date - date_time
		#print time_difference # This time_difference might not be accurate if it was from a recursive call
		train_type = get_train_type(schedule, direction, station, next_time)
		train_id = get_train_id(schedule, direction, station, next_time)
		return next_time_date, train_type, train_id # Date time object
	else:
		# Wrap around to tomorrow's schedule.
		tomorrow = date_time + datetime.timedelta(days = 1)
		tomorrow_midnight = datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day, 0, 0, 0, 0)
		tomorrow_schedule = determine_schedule_type(tomorrow)
		first_time_tomorrow = next_time_params(direction, station, tomorrow_midnight) # Recursive call
		#first_time_tomorrow_date = datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day, first_time_tomorrow.hour,
		#							first_time_tomorrow.minute, first_time_tomorrow.second, first_time_tomorrow.microsecond)
		#time_difference =  first_time_tomorrow_date - date_time
		#print time_difference # Time delta
		return first_time_tomorrow

def time_difference_mins(train_datetime):
	if train_datetime == "skip":
		return "--"

	today_datetime = datetime.datetime.now()
	difference = train_datetime - today_datetime # Train hasn't arrived yet --> positive
	seconds = difference.total_seconds()
	minutes_away = int(math.ceil(seconds / 60.0))

	if abs(minutes_away) == 1:
		minutes_form = "minute"
	else:
		minutes_form = "minutes"

	if abs(minutes_away) == 0:
		return "now"

	if minutes_away >= 0: 
		return ("%d " + minutes_form + " away") % abs(minutes_away)
	else:
		return ("%d " + minutes_form + " ago") % abs(minutes_away)

# Must convert for lookup in dictionary of times!
def datetime_to_time(date_time):
	return datetime.time(date_time.hour, date_time.minute, 0, 0)

def time_to_datetime(time, date):
	# Time on given date blended into a datetime 
	return datetime.datetime(date.year, date.month, date.day, time.hour, time.minute, time.second, time.microsecond)

# Returns a datetime! 
def next_time(direction, station):
	date_time = datetime.datetime.now()
	return next_time_params(direction, station, date_time)

# Returns a datetime!
def prev_time(direction, station):
	date_time = datetime.datetime.now()
	return prev_time_params(direction, station, date_time)

# n >= 1
def get_nth_time_params(direction, station, date_time, n):
	result = next_time_params(direction, station, date_time) # Next time
	# Loop will not be executed if n = 1
	for i in range(n - 1):
		next_start_time = result[0] + datetime.timedelta(microseconds = 1)
		result = next_time_params(direction, station, next_start_time)
		# Check the next time, with a start point of immediately after the next stop

	return result

def get_nth_time(direction, station, n):
	result = next_time(direction, station)
	# Loop will not be executed if n = 1
	for i in range(n - 1):
		next_start_time = result[0] + datetime.timedelta(microseconds = 1)
		result = next_time_params(direction, station, next_start_time)

	return result

# n >= 1
def get_nth_prev_time_params(direction, station, date_time, n):
	result = prev_time_params(direction, station, date_time)
	# Loop will not be executed if n = 1
	for i in range(n - 1):
		prev_start_time = result[0] - datetime.timedelta(microseconds = 1)
		result = prev_time_params(direction, station, prev_start_time)

	return result

def get_nth_prev_time(direction, station, n):
	result = prev_time(direction, station)
	# Loop will not be executed if n = 1
	for i in range(n - 1):
		prev_start_time = result[0] - datetime.timedelta(microseconds = 1)
		result = prev_time_params(direction, station, prev_start_time)

	return result

# If n <= 0: get_nth_prev_time with n = 1 + abs(n)
# If n > 0: get_nth_time (next) with n = n
def get_nth_time_combined(direction, station, n):
	if (n > 0): 
		return get_nth_time(direction, station, n)
	else:
		prev_n = abs(n) + 1
		return get_nth_prev_time(direction, station, prev_n)

# Data formatted for templating!
# Returns Time (AM/PM), minutes away, type, ID
def get_nth_time_formatted(direction, station, n):
	old_result = get_nth_time(direction, station, n)
	date_time = old_result[0]
	date_time_now = datetime.datetime.now()
	date_time_formatted = format_time(date_time)

	minutes_away = time_difference_mins(date_time)

	return date_time_formatted, minutes_away, old_result[1], old_result[2]

def get_route_type(route_id):
	route_list = data['routes'][route_id]
	route_type = route_list[0]
	return route_type

def get_route_direction(route_id):
	id_split = route_id.split('_')
	if len(id_split) == 3:
		direction = 'tottenville'
	else:
		direction = 'st_george'
	return direction

# Return 3-tuple schedule_number, schedule, direction, all strings (e.g. ["12", "weekday", "tottenville"])
def parse_route_id(route_id):
	id_split = route_id.split('_')
	if len(id_split) == 3:
		direction = 'tottenville'
	else:
		direction = 'st_george'
	schedule_number = id_split[0]
	schedule = id_split[1]
	return schedule_number, schedule, direction

# Algorithm thoughts 
# For trian route page:
# Given: Route ID which implies #, Station, Direction
# First check train's origin schedule. Is it equal to today's schedule? If yes, it's from today
# What if it is a train left over from yesterday's schedule? 
# This can occur if the train's start time was after ~11:30PM (lookup exact) and its last stop was after 12:00AM (0:00) and its origin schedule was from yesterday.
# Only proceed if last two conditions are met (it is a candidate for running: Either from late yesterday wrap or today.)
# Don't forget to account for yesterday and today wrap. 
# Remember what made it proceed to this state: was it a yesterday or today train?
# If it was a yesterday train, mark non-12:00AM (11:00PM) times with yesterday's date and the 12:00AM with today's.
# If it was a today train: --
#	If it was a wraparound train: (Start time 11:00, end time after 12) 11 with today's, 12 with tomorrow's
# 	If it was not a wraparound train: (others) All with todays 
# Train times now marked with date. Easy true relative position can now be determined with today's datetime, as well if it's actually running.
# A train only made it to this stage if it was a candidate for running.
# Use the times to get if it's actually running as well as position and times away

# Given Route ID, get the route_list datestamped based on today, if it is possible for it to exist
def date_stamp_route(train_id):
	id_split = train_id.split('_')
	direction = get_route_direction(train_id)
	schedule = id_split[1]

	today_datetime = datetime.datetime.now()
	yesterday_datetime = today_datetime - datetime.timedelta(days = 1)
	tomorrow_datetime = today_datetime + datetime.timedelta(days = 1)

	yesterday_schedule = determine_schedule_type(yesterday_datetime)
	today_schedule = determine_schedule_type(today_datetime)
	tomorrow_schedule = determine_schedule_type(tomorrow_datetime)

	unmarked_route = data['routes'][train_id][1]

	# There are no wraparound trains with skips in them. 

	first_time = unmarked_route[0]
	last_time = unmarked_route[-1]

	if first_time == "skip" or last_time == "skip":
		wraparound_train = False
	else:
		wraparound_train = (first_time.hour == 23) and (last_time.hour == 0)

	# Candidate check
	if (schedule == today_schedule):
		if wraparound_train:
			# It could've been a wraparound train that started today (the last of today's), or 
			# it could've been a wraparound train that started yesterday (and yesterday had the same schedule) that wrapped to today.
			# Look at today's time: If today just started, refer to it as a yesterday originator.
			# If today is closer to ending, refer to it as a today originator. 
			# Arbitrarily set the threshold to noon.
			past_noon = today_datetime.hour >= 12
			if past_noon:
				# Use today originator. 
				# 23's marked with today, 00's marked with tomorrow 
				marker_23 = today_datetime
				marker_00 = tomorrow_datetime
			else:
				# Use yesterday originator. 
				# 23's marked with yesterday, 00's marked with today.
				marker_23 = yesterday_datetime
				marker_00 = today_datetime

			new_times_list = []

			for time in unmarked_route:
				if time != "skip":
					if time.hour == 23:
						new_date_time = time_to_datetime(time, marker_23)
					elif time.hour == 0:
						new_date_time = time_to_datetime(time, marker_00)
				else:
					new_date_time = "skip"

				new_times_list.append(new_date_time)

			return new_times_list
		else:
			# Standard today train, all times marked with today's date.
			new_times_list = []

			for time in unmarked_route:
				if time != "skip":
					new_date_time = time_to_datetime(time, today_datetime)
				else:
					new_date_time = "skip"

				new_times_list.append(new_date_time)

			return new_times_list


	elif (wraparound_train and (schedule == yesterday_schedule)):
			# We know for sure it was from yesterday.
			marker_23 = yesterday_datetime
			marker_00 = today_datetime

			new_times_list = []

			for time in unmarked_route:
				if time != "skip":
					if time.hour == 23:
						new_date_time = time_to_datetime(time, marker_23)
					elif time.hour == 0:
						new_date_time = time_to_datetime(time, marker_00)
				else:
					new_date_time = "skip"

				new_times_list.append(new_date_time)	

			return new_times_list
	else:
			# Not a candidate for running
		return False

def is_running(train_id):
	stamped_route = date_stamp_route(train_id)
	if stamped_route == False:
		# If it didn't meet the condition for having a stamped route
		# (Not even a candidate for running)
		return False
	else:

		first_time = "skip"
		last_time = "skip"

		# The while loops are for the purpose of "zoning in" 
		# on start and end times if the train starts/ends at a point 
		# on the line that is not the original terminal and hence 
		# would be marked "skip" for that location and any others that it skips

		i = 0
		while (first_time == "skip"):
			first_time = stamped_route[i]
			i += 1

		j = -1
		while (last_time == "skip"):
			last_time = stamped_route[j]
			j -= 1

		time_now = datetime.datetime.now()
		return (time_now >= first_time and time_now <= last_time)

def last_stop(route):
	times = date_stamp_route(route)
	time_now = datetime.datetime.now()

	counter = -1
	for time in times:
		if time == "skip":
			counter += 1
		elif time_now > time:
			counter += 1
		else:
			break
	# Made it all the way across
	if counter < 0:
		counter = 0
	
	direction = parse_route_id(route)[2]

	if direction == "tottenville":
		return timescraper.to_tottenville_list[counter]
	else:
		return timescraper.to_st_george_list[counter]

#####################################################################################

### Printing and Data Packaging for Flask ###

# Not Dated - Just for a general, standard route times page
def print_route_times(route):
	direction = get_route_direction(route)
	times = data['routes'][route][1]

	if direction == 'tottenville':

		for stop in timescraper.to_tottenville_list:
			
			time = times[timescraper.to_tottenville_list.index(stop)]
			formatted_stop = format_stop(stop)

			print formatted_stop + ":", format_time(time)

	else:

		for stop in timescraper.to_st_george_list:
			
			time = times[timescraper.to_st_george_list.index(stop)]
			formatted_stop = format_stop(stop)

			print formatted_stop + ":", format_time(time)

	return

# Dated - Precondition: route is candidate for running
# Gives the previous train + the next three.
# (For the previous train + the next n, use range n + 1)
# (No previous train: start interval with 1)
# (Additional previous trains: extend into negatives)

# Reminder: get_nth_time functions return (datetime_object_of_stoptime, train_type, train_id)
def print_dated_station_times(direction, station):
	for i in range():
		data_tuple = get_nth_time_combined(direction, station, i)

		stop_time = data_tuple[0]
		formatted_stop_time = format_time(stop_time)
		delta = time_difference_mins(stop_time)
		train_type = data_tuple[1]
		train_id = data_tuple[2]

		print formatted_stop_time, delta, train_type, train_id


def determine_train_label(train_type):
	print train_type
	if train_type == "A" or train_type == "C":
		return "regular"
	elif train_type == "B" or train_type == "D" or train_type == "F":
		return "express"
	else:
		return "great_kills"


def get_label_html(label):
	if label == "regular":
		return '<span class="label label-default">Regular</span>'
	elif label == "express":
		return '<span class="label label-success">Express</span>'
	else:
		return '<span class="label label-info">Great Kills</span>'

# Returns dated station times in list form. A list of dictionaries that contain associated information for each upcoming train.
# ['stop_time': formatted_stop_time, 'delta': delta, 'type': train_type, 'label': label_html, 'id': train_id]
def station_package(direction, station):
	package = []
	for i in range(4):
		data_tuple = get_nth_time_combined(direction, station, i)

		stop_time = data_tuple[0]
		formatted_stop_time = format_time(stop_time)
		delta = time_difference_mins(stop_time)
		train_type = data_tuple[1]
		label = determine_train_label(train_type)
		label_html = get_label_html(label)
		train_id = data_tuple[2]

		this_time_list = {'stop_time': formatted_stop_time, 'delta': delta, 'type': train_type, 'label': label_html, 'id': train_id}
		package.append(this_time_list)
		print this_time_list 
	return package

# Given a route, determines the last stop to have been visited (based on train's current location or time now)
# Pre-condition: train is running
def get_formatted_time_now():
	time_now = datetime.datetime.now()
	return format_time(time_now)

# Dated - Precondition: route is candidate for running
def print_dated_route_times(route):
	direction = get_route_direction(route)
	times = date_stamp_route(route)

	if direction == 'tottenville':

		for stop in timescraper.to_tottenville_list:
			
			time = times[timescraper.to_tottenville_list.index(stop)]
			delta = time_difference_mins(time)
			formatted_stop = format_stop(stop)

			print formatted_stop + ":", format_time(time), delta

	else:

		for stop in timescraper.to_st_george_list:
			
			time = times[timescraper.to_st_george_list.index(stop)]
			delta = time_difference_mins(time)
			formatted_stop = format_stop(stop)

			print formatted_stop + ":", format_time(time), delta

	return

def get_station_url(station):
	return "/station/" + station

def get_direction_html(direction):
	if direction == "st_george":
		return '<span class="label label-danger">To St George</span>'
	else:
		return '<span class="label label-warning">To Tottenville</span>'

def format_train_id(train_id):
	info_tuple = parse_route_id(train_id)
	number = info_tuple[0]
	schedule = info_tuple[1]
	direction = info_tuple[2]

	if direction == "st_george":
		direction_formatted = "St George"
	else:
		direction_formatted = "Tottenville"

	if schedule == "weekday":
		schedule_formatted = "Weekday"
	elif schedule == "saturday":
		schedule_formatted = "Saturday"
	else:
		schedule_formatted = "Sunday"

	return schedule_formatted + " #" + number

# Returns dated route times page package
def dated_route_times_package(route):

	times = date_stamp_route(route)
	is_candidate = times

	direction = get_route_direction(route)
	
	if is_running(route):
		previous_stop = format_stop(last_stop(route))
	else:
		previous_stop = False

	
	route_type = get_route_type(route)
	label_html = get_label_html(determine_train_label(route_type))
	direction_html = get_direction_html(direction)
	formatted_name = format_train_id(route)

	route_info_package = {'name': formatted_name, 'is_candidate': is_candidate,
		'previous_stop': previous_stop, 'type': route_type, 'label_html': label_html, 'direction_html': direction_html}

	package = [route_info_package]


	if is_candidate:
		if direction == 'tottenville':

			times_package = []

			for stop in timescraper.to_tottenville_list:
				
				unformatted_time = times[timescraper.to_tottenville_list.index(stop)]
				time = format_time(unformatted_time)
				delta = time_difference_mins(unformatted_time)
				formatted_stop = format_stop(stop)
				stop_url = get_station_url(stop)


				if time == "--":
					skipped = True
				else:
					skipped = False

				stop_dict = {'stop': formatted_stop, 'stop_id': stop, 'url': stop_url, 'time': time, 'delta': delta, 'skipped': skipped}
	#  'type': route_type,
	#				'label_html': label_html, 'direction_html': direction_html 
				times_package.append(stop_dict)

			package.append(times_package)

		else:

			times_package = []

			for stop in timescraper.to_st_george_list:

				unformatted_time = times[timescraper.to_st_george_list.index(stop)]
				time = format_time(unformatted_time)
				delta = time_difference_mins(unformatted_time)
				formatted_stop = format_stop(stop)
				stop_url = get_station_url(stop)
				
				if time == "--":
					skipped = True
				else:
					skipped = False

				stop_dict = {'stop': formatted_stop, 'stop_id': stop, 'url': stop_url, 'time': time, 'delta': delta, 'skipped': skipped}

				times_package.append(stop_dict)

			package.append(times_package)

	return package

def get_previous_station(station):
	station_index = timescraper.to_st_george_list.index(station)
	previous_station_index = station_index - 1
	if previous_station_index < 0:
		return False
	else:
		return timescraper.to_st_george_list[previous_station_index]

def get_next_station(station):
	station_index = timescraper.to_st_george_list.index(station)
	next_station_index = station_index + 1 
	if next_station_index > (len(timescraper.to_st_george_list) - 1):
		return False
	else:
		return timescraper.to_st_george_list[next_station_index]


#####################################################################################

### Assorted Tests ###

#print data['routes']['44_weekday_st_george'][1][timescraper.to_st_george_list.index('st_george')]
#print (next_time_params('tottenville', 'grasmere', datetime.datetime(2014, 7, 11, 23, 49, 0, 0)))
#print next_time('st_george', 'princes_bay')
#print get_nth_time('st_george', 'princes_bay', 2)
#for i in range(1, 5):
#	print get_nth_prev_time_params('st_george', 'princes_bay', datetime.datetime(2014, 7, 9, 0, 45, 0, 0), i)
#print prev_time('st_george', 'princes_bay')
#for i in range(1,10):
#	print get_nth_time_formatted('st_george', 'eltingville', i)
#print date_stamp_route("73_weekday_tottenville")
#for i in range(74):
#	print is_running(str(i) + "_sunday_st_george")
#for i in range(78):
#	print_dated_route_times(str(i) + "_weekday_tottenville")
#print get_nth_time('tottenville', 'princes_bay', 1)
#print dated_route_times_package('0_weekday_tottenville')

#for station in timescraper.to_st_george_list:
#	print '<a href="' + './station/' + station + '"><button type="button" class="btn btn-default"> ' + format_stop(station) + '</button></a>'
#	print '<a type="button" href="./station/' + station + '" ' + 'class="btn btn-default"> ' + format_stop(station) + '</a>'
#print is_running('73_weekday_tottenville') #called on Saturday