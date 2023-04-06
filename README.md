# Weather Data from Open Meteo API

This repository contains a tool to easily access weather data using the Open Meteo API. By specifying a location and a time period, you can import **historic** and **upcoming** **hourly** weather data from around the world with **different measurements** such as temperature, rain, snow, wind and more.

The weather data comes from the Open Meteo API:

*   The Open Meteo Archive API, which provides historical weather data
*   The Open Meteo Forecast API, which provides forecasted weather data

**https://open-meteo.com/en/docs**

## Usage

The script contains four functions:

*   **get_latest_recorded_date()** - Returns the latest recorded date in the Open Meteo Archive API database.
*   **get_archived_weather(lat, long, start, end, metrics)** - Returns historical weather data for a given latitude and longitude, time range, and set of metrics.
*   **get_forecast_weather(lat, long, metrics)** - Returns forecasted weather data for a given latitude and longitude and set of metrics.
*   **get_distance(lon1, lat1, lon2, lat2)** - returns the distance in kilometers between two sets of longitude and latitude coordinates.

To use any of these functions, simply import the weather_data.py file and call the desired function with the appropriate parameters.

## Example

Here's an example of how to use the **`get_archived_weather()`** function to retrieve historical weather data for a location:

```python
import weather_data

lat = 43.296482 # Marseille latitude
long = 5.36978 # Marseille longitude
start = '2023-03-01'
end = '2023-03-25'
metrics = ['temperature', 'precipitation']

data = weather_data.get_archived_weather(lat, long, start, end, metrics)
```

This will return a dictionary containing **hourly** weather data for Marseille for the month of March 2023, including temperature and precipitation metrics.

Then you can view the data in the form of a dataframe as follows:

```python
import pandas as pd

pd.DataFrame(data)
```

```
>>      latitude  longitude              time  temperature_2m  precipitation
   0    43.40001   5.300003  2023-03-01T00:00             4.5            0.0
   1    43.40001   5.300003  2023-03-01T01:00             4.1            0.0
   2    43.40001   5.300003  2023-03-01T02:00             3.7            0.0
   3    43.40001   5.300003  2023-03-01T03:00             3.1            0.0
   ..        ...        ...               ...             ...            ...
   596  43.40001   5.300003  2023-03-25T20:00            13.0            0.0
   597  43.40001   5.300003  2023-03-25T21:00            12.4            0.0
   598  43.40001   5.300003  2023-03-25T22:00            11.5            0.0
   599  43.40001   5.300003  2023-03-25T23:00            11.7            0.0
```


If you want to import weather data for different locations, you can do the following (with or without multiprocessing):

```python
from multiprocessing import Pool
from functools import partial

params = [(48.85826,   2.294499),  # Eiffel Tower coordinates
          (40.689253, -74.044547), # Statue of Liberty coordinates
          (27.175012,  78.042097)] # Taj Mahal coordinates

start = '2023-03-01'
end = '2023-03-25'
metrics = ['snowfall', 'windspeed_10m']

with Pool(4) as pool:
    data = pool.starmap(partial(weather_data.get_archived_weather, start=start, end=end, metrics=metrics),
                        params)

pd.concat([pd.DataFrame(d) for d in data])
```

```
>>       latitude  longitude              time  snowfall  windspeed_10m
   0    48.900010   2.300003  2023-03-01T00:00       0.0           14.7
   1    48.900010   2.300003  2023-03-01T01:00       0.0           15.1
   2    48.900010   2.300003  2023-03-01T02:00       0.0           15.1
   3    48.900010   2.300003  2023-03-01T03:00       0.0           14.7
   ..         ...        ...               ...       ...            ...
   596  27.200005  78.000000  2023-03-25T20:00       0.0            6.9
   597  27.200005  78.000000  2023-03-25T21:00       0.0            8.2
   598  27.200005  78.000000  2023-03-25T22:00       0.0           11.9
   599  27.200005  78.000000  2023-03-25T23:00       0.0           12.8
```

## Credits

This repository is maintained by Antoine PINTO (antoine.pinto1@outlook.fr). It is based on the Open Meteo API, which provides the weather data.