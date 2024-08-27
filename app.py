from flask import Flask, jsonify, request, render_template
from FlightRadar24 import FlightRadar24API
import logging
import traceback

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
fr_api = FlightRadar24API()  # Move this outside of the route function

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/get_flights')
def get_flights():
    try:
        lat = float(request.args.get('lat'))
        lon = float(request.args.get('lon'))
        radius = float(request.args.get('radius', 40000))  # Add radius parameter with default value
        
        app.logger.debug(f"Received request for lat: {lat}, lon: {lon}, radius: {radius}")
        
        bounds = fr_api.get_bounds_by_point(lat, lon, radius)
        flights = fr_api.get_flights(bounds=bounds)
        app.logger.debug(f"Number of flights found: {len(flights)}")
        
        flight_data = [{
            'callsign': flight.callsign,
            'altitude': flight.altitude,
            'speed': flight.ground_speed,
            'latitude': flight.latitude,  # Add latitude
            'longitude': flight.longitude  # Add longitude
        } for flight in flights]
        
        return jsonify(flight_data)
    
    except ValueError as ve:
        app.logger.error(f"Invalid input: {str(ve)}")
        return jsonify({"error": "Invalid input parameters"}), 400
    except Exception as e:
        app.logger.error(f"An error occurred: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True)
    