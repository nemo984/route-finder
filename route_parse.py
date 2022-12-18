import csv
import collections
from pyswip import Prolog, Atom
from util import bidict

routes = []
stations = {} # key - station name, value - station
station_name_map = bidict({}) # key: station name, value: station fact name 

class Station:
    def __init__(self, name, identifier, station_type):
        self.name = name
        self.p = identifier
        self.type = station_type
    
    def fact_value(self):
        return self.p

    def __str__(self):
        return self.name
    
    def fact(self):
        return f"station({self.fact_value()}, {self.type})"

class Route:
    def __init__(self, from_station, to_station, duration):
        assert isinstance(from_station, Station)
        assert isinstance(to_station, Station)
        self.from_station = from_station
        self.to_station = to_station
        self.duration = duration

    def __str__(self):
        return f"From {self.from_station} to {self.to_station}"

    def fact(self):
        return f"route({self.from_station.fact_value()}, {self.to_station.fact_value()}, {self.duration})"

prolog = Prolog()
def parse_routes():
    parse_routes_data("./data/bts/bts_routes.csv", "bts")
    parse_routes_data("./data/mrt/mrt_blue_routes.csv", "mrt_blue")
    parse_routes_data("./data/mrt/mrt_purple_routes.csv", "mrt_purple")
    parse_routes_data("./data/bts_mrt_routes.csv", "bts_mrt")
    for station in stations.values():
        if station.type == "bts_mrt":
            continue
        station_name_map[station.name] = station.fact_value()
        print(station.fact() + ".")
        prolog.assertz(station.fact())

    for route in routes:
        print(route.fact() + ".")
        prolog.assertz(route.fact())
    prolog.consult("knowledge.pl")

Path = collections.namedtuple('Path', ['path', 'time', 'cost', 'stops'])
def shortest_path(start, end):
    start = station_name_map[start]
    end = station_name_map[end]
    result = prolog.query(f"shortest_path({start}, {end}, Path, Time, Cost, Stops)")
    try:
        result = next(result)
        path = [stations[station_name_map.inverse[str(station)][0]] for station in result["Path"]]
        return Path(path, result["Time"], result["Cost"], result["Stops"])
    except StopIteration:
        return Path(None, 0, 0)

def parse_routes_data(path, route_type):
    with open(path) as f:
        reader = csv.reader(f)
        for route in reader:
            from_station = route[0].strip()
            from_station_name = from_station.replace("_", " ")
            to_station = route[1].strip()
            to_station_name = to_station.replace("_", " ")
            duration = int(route[2].strip())
            s1 = stations[from_station_name] if from_station_name in stations else \
                stations.setdefault(from_station_name, Station(from_station_name, from_station.lower(), route_type))
            s2 = stations[to_station_name] if to_station_name in stations else \
                stations.setdefault(to_station_name, Station(to_station_name, to_station.lower(), route_type))
            routes.append(Route(s1, s2, duration)) 
            routes.append(Route(s2, s1, duration)) 

def get_stations():
    return [station.name for station in stations.values()]

if __name__ == "__main__":
    parse_routes()
    while True:
        try:
            from_point = input("Enter the starting point: ")
            to_point = input("Enter the ending point: ")
            shortest_path(from_point, to_point)
        except ValueError as error:
            print(error)
