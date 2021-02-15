import json
import requests


class CarbonInterface:

    API = "https://www.carboninterface.com/api/v1/"

    def __init__(self, api_key, units="kg"):
        f"""Connect to {self.API}

        Parameters:
        - api_key: required
        - units ("g", "lb", "kg", "mt"): carbon estimate unit value, defaults to kg
        """
        self.api_key = api_key
        self.units = units
        self._authenticate()

    def __repr__(self):
        return f"CarbonInterface(units='{self.units}')"

    def _authenticate(self):
        """Authenticate API connection"""
        url = f"{self.API}/auth"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.get(url, headers=headers)
        print(response)

    @property
    def _headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def post(self, data):
        """Query /estimates endpoint

        Parameters:
        - data: dictionary (see API docs for details)

        Returns:
        - dictionary of API response
        """
        json_data = json.dumps(data)
        url = f"{self.API}/estimates"
        response = requests.post(url, data=json_data, headers=self._headers)
        return response.json()

    def _extract_value(self, response_json):
        rd = response_json["data"]
        value = rd["attributes"][f"carbon_{self.units}"]
        return value

    def estimate_flight(self, departure, destination, round_trip=False):
        f"""Estimate carbon emissions for an economy flight

        Parameter:
        - departure: IATA airport code
        - destination: IATA airport code
        - round_trip (True, False): calculate round trip, defaults to False

        Returns:
        - estimated carbon emissions in {self.units}
        """

        legs = [{"departure_airport": departure, "destination_airport": destination}]

        if round_trip:
            legs.append(
                {
                    "departure_airport": destination,
                    "destination_airport": departure,
                }
            )

        data = {"type": "flight", "passengers": 1, "legs": legs}
        response_json = self.post(data)
        value = self._extract_value(response_json)
        return value

    def estimate_electricity(self, amount, unit="mwh", country="us", state=None):
        f"""Estimate carbon emissions for an amount of electricity consumed

        Parameters:
        - amount: of electricity consumption
        - unit ("mwh", "kwh"): of electricity consumption, defaults to "mwh"
        - country ("ca", "us"): supports Canada and United States, defaults to "us"
        - state (optional): two letter ISO state/province

        Returns:
        - estimated carbon emissions in {self.units}
        """

        data = {
            "type": "electricity",
            "electricity_value": amount,
            "electricity_unit": unit,
            "country": country,
        }

        if state:
            data["state"] = state

        response_json = self.post(data)
        value = self._extract_value(response_json)
        return value

    def estimate_shipping(
        self, weight, distance, method="truck", weight_unit="g", distance_unit="km"
    ):
        f"""Estimate carbon emissions for a package

        Features:
        - weight: weight of package in weight_unit(s)
        - distance: distance travelled by package in distance_unit(s)
        - method ("truck", "ship", "train", "plane"): of transportation, defaults to "truck"
        - weight_unit ("g", "lb", "kg", "mt"): defaults to "g"
        - distance_unit ("km", "m"): defaults to "km"

        Returns:
        - estimated carbon emissions in {self.units}
        """

        data = {
            "type": "shipping",
            "weight_value": weight,
            "weight_unit": weight_unit,
            "distance_value": distance,
            "distance_unit": distance_unit,
            "transport_method": method,
        }

        response_json = self.post(data)
        value = self._extract_value(response_json)
        return value
