from get_departure import FutarAPI, DepartureLoader
from timer_visualizer import Visualizer
from datetime import datetime
from datetime import date
import time
import json
import traceback


with open("config.json", "r") as file:
    config = json.load(file)


api = FutarAPI(config["api_key"])  # get api key at https://opendata.bkk.hu/
departure_loader = DepartureLoader(api)
stop_id = departure_loader.find_stop_id(config["stop_finding"]["name"], config["stop_finding"]["lat"], config["stop_finding"]["lon"], config["stop_finding"]["radius"])
departures = departure_loader.get_departures(stop_id)

last_refresh = time.time()
refresh_diffs = []
keep_n_refresh_diffs = config["keep_n_refresh_diffs"]
max_average_refresh_diff_seconds = config["max_average_refresh_diff_seconds"]

refresh_rate = config["refresh_rate"]


visualizer = Visualizer()



prev_start_time = 0
prev_time = 0
while True:
    try:
        start = time.time()
        
        now = datetime.now()
        departureDeltas = []
        for departure in departures:
            if departure >= now:
                delta = departure - now 
                total_seconds = int(delta.total_seconds())
                
                departureDeltas.append(total_seconds)
        
        if len(departureDeltas) == 0 or start - last_refresh > refresh_rate:
            departures = departure_loader.get_departures(stop_id)
            
            refresh_diffs.append(time.time() - last_refresh)
            if len(refresh_diffs) > keep_n_refresh_diffs:
                refresh_diffs.pop(0)
            average_refresh_diff = sum(refresh_diffs) / keep_n_refresh_diffs
            if average_refresh_diff < max_average_refresh_diff_seconds:
                raise Exception("Too frequent api calls")
            
            last_refresh = time.time()
            continue

        nextDeparture = min(departureDeltas)
        minutes, seconds = divmod(abs(nextDeparture), 60)
        time_str = f"{minutes:02}:{seconds:02}"
        
        if nextDeparture > prev_time:
            prev_start_time = nextDeparture
        
        ratio = 1 - (nextDeparture / prev_start_time)
        
        visualizer.refresh(time_str, ratio)
        
        time.sleep(1 - (time.time() - start))
        prev_time = nextDeparture
    except:
        visualizer.refresh("Error!")
        traceback.print_exc()
        time.sleep(10)
    
    
