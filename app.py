from flask import Flask, jsonify, request, render_template
from  FlightRadar24 import FlightRadar24API
import logging
import traceback

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/get_flights')
def get_flights():
    try:
        lat = float(request.args.get('lat'))
        lon = float(request.args.get('lon'))
        # ran = float(request.args.get('ran'))
        
        app.logger.debug(f"Received request for lat: {lat}, lon: {lon}")
        fr_api = FlightRadar24API()
        bounds = fr_api.get_bounds_by_point(lat, lon, 40000)
        # app.logger.debug(f"Calculated bounds: {bounds}")
        
        flights = fr_api.get_flights(bounds=bounds)
        app.logger.debug(flights)
        app.logger.debug(f"Number of flights found: {len(flights)}")
        
        # Process the flights data to extract relevant information
        flight_data = []
        for flight in flights:
            flight_data.append({
                'callsign': flight.callsign,
                'altitude': flight.altitude,
                'speed': flight.ground_speed
            })
        
        return jsonify(flight_data)
    
    except Exception as e:
        app.logger.error(f"An error occurred: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)