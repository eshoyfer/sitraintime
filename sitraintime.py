from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

import os
import engine

app = Flask(__name__)

# Assorted Functions


# Routing + Views

@app.route('/')
def index():
    return render_template("home.html")

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/station/<station>')
def station(station):
	try:
		station_name = engine.format_stop(station)
	except:
		abort(404)

	last_updated = engine.get_formatted_time_now()

	# station_package(station, direction)

	# Returns dated station times in list form. A list of dictionaries that contain associated information for each upcoming train.
	# ['stop_time': formatted_stop_time, 'delta': delta, 'type': train_type, 'label': label_html, 'id': train_id]

	to_st_george = engine.station_package('st_george', station)
	to_tottenville = engine.station_package('tottenville', station)

	next_station = engine.get_next_station(station)
	prev_station = engine.get_previous_station(station)

	return render_template("station.html", station_name=station_name, last_updated=last_updated, st_george=to_st_george, tottenville=to_tottenville, test="<b>test</b>",
		prev=prev_station, next=next_station)

@app.route('/train/<train_id>')
def train(train_id):
	last_updated = engine.get_formatted_time_now()

	try:
		package = engine.dated_route_times_package(train_id)
	except:
		abort(404)

	route_info_package = package[0]

	is_on_today_schedule = route_info_package['is_candidate']

	previous_stop = route_info_package['previous_stop']
	is_running = previous_stop

	direction_html = route_info_package['direction_html']
	label_html = route_info_package['label_html']

	name = route_info_package['name']

	if is_on_today_schedule:
		station_times = package[1] # List of dicts
	else:
		station_times = False

	return render_template('train.html', name=name, last_updated=last_updated, is_running=is_running, previous_stop=previous_stop, is_on_today_schedule=is_on_today_schedule,
		station_times=station_times, direction_html=direction_html, label_html=label_html)

@app.errorhandler(404)
def not_found(e): # Return rendering, 404
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e): # Return rendering, 500
	return render_template('500.html'), 500
# Run

# Uncomment for local tests:

#if __name__ == '__main__':
#   app.run(debug=True)
#	app.run(host='0.0.0.0')