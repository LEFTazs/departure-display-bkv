import requests
from datetime import datetime
from datetime import date


class FutarAPI:
    def __init__(self, key):
        self.baseurl = "https://futar.bkk.hu/api/query/v1/ws/otp"
        self.key = key
    
    def call(self, endpoint, params):
        response = requests.get(f"{self.baseurl}{endpoint}?key={self.key}", params=params)
        return response.json()


class DepartureLoader:
    def __init__(self, api):
        self.api = api
    
    def find_stop_id(self, stop_name_to_find, lat_to_find, lon_to_find, search_radius):
        stop_position_to_find = {"lat": lat_to_find, "lon": lon_to_find, "radius": search_radius}
        stops = self.api.call("/api/where/stops-for-location", stop_position_to_find)
        found_stop_id = None
        for stop in stops["data"]["list"]:
            if stop["name"] in stop_name_to_find:
                found_stop_id = stop["id"]
        assert found_stop_id is not None, "Stop not found"
        return found_stop_id
    
    def get_departures(self, stop_id):
        today = date.today().strftime("%Y%m%d")
        params = {
            "stopId": stop_id,
            "date": today,
            "onlyDepartures": "false",
            "includeReferences": "true",
        }
        data = self.api.call("/api/where/schedule-for-stop", params)


        directionIdToUse = "1"
        foundDirection = None
        for schedule in data['data']["entry"]['schedules']:
            for direction in schedule["directions"]:
                if direction["directionId"] == directionIdToUse:
                    foundDirection = direction
                    break
        assert foundDirection is not None, "Direction not found at stop with given id"

        departures = []
        for st in foundDirection["stopTimes"]:
            dt = datetime.fromtimestamp(st["departureTime"])
            departures.append(dt)
        return departures
