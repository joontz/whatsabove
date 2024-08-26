from flightradar24 import FlightRadar24API


fr_api = FlightRadar24API(...)


bounds = fr_api.get_bounds_by_point(39.0306634, -94.577041, 4000)

flights = fr_api.get_flights(bounds = bounds)

print(flights)