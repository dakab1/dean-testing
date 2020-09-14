from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from deantest.settings import OPERNWEATHERMAP_KEY, OPENWEATHER_API_URL
import requests
import statistics

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


def aggrigateStats(records):

    minTemperature = None
    maxTemperature = None
    avgTemperature = None
    medTemperature = None
    temperature = []
    temperatureMin = []
    temperatureMax = []

    minHumidity = None
    maxHumidity = None
    avgHumidity = None
    medHumidity = None
    humidity = []

    for record in records:
        temperature.append(record['main']['temp'])
        humidity.append(record['main']['humidity'])
        temperatureMin.append(record['main']['temp_min'])
        temperatureMax.append(record['main']['temp_max'])

    # Computes min, max, average and median temperature and humidity for that location and period and returns that to the user
    avgTemperature = statistics.mean(temperature)
    avgHumidity = statistics.mean(humidity)

    medHumidity = statistics.median(humidity)
    medTemperature = statistics.median(temperature)

    maxHumidity = max(humidity)
    maxTemperature = max(temperatureMax)

    minHumidity = min(humidity)
    minTemperature = min(temperatureMin)

    # Respond with json of aggrigated data
    return {'avgTemperature': avgTemperature, 'avgHumidity': avgHumidity, 'medHumidity': medHumidity, 'medTemperature': medTemperature, 'maxHumidity': maxHumidity, 'maxTemperature': maxTemperature,  'minHumidity': minHumidity, 'minTemperature': minTemperature}


@api_view(('GET',))
def forecast(APIView, city):

    # TODO: Validate input

    # Query rest service
    url = None
    if 'period' not in APIView.query_params:

        url = '%sweather?q=%s&appid=%s&units=metric' % (
            OPENWEATHER_API_URL, city, OPERNWEATHERMAP_KEY)

    elif APIView.query_params['period'].isnumeric():

        # Openweathermap cnt param. Each one represents 3 hours more. e.g, if you want 9 hours ahead set this to 3
        cnt = APIView.query_params['period']  # TODO: Check if this is clean

        # Set cnt parameter to control number of rows returned
        url = '%sforecast?q=%s&appid=%s&units=metric&cnt=%s' % (
            OPENWEATHER_API_URL, city, OPERNWEATHERMAP_KEY, cnt)

    else:

        # Error http 400 bad request error
        return Response({'message': 'invalid period'}, status=status.HTTP_400_BAD_REQUEST)

    logger.info('Sending request to %s' % url)
    r = requests.get(url)

    logger.debug('response code is %s' % r.status_code)

    if r.status_code == 200:

        jsonData = r.json()
        logger.debug('json response is %s' % jsonData)

        weatherData = []
        if 'list' in jsonData:
            weatherData = jsonData['list']
        elif 'main' in jsonData:
            weatherData.append(jsonData)

        # Computes min, max, average and median temperature and humidity for that location and period and returns that to the user
        aggrigated = aggrigateStats(weatherData)

        # Format response and send
        return Response(data={'data': weatherData, 'aggrigated': aggrigated}, status=status.HTTP_200_OK)

    elif r.status_code == 404:

        # Return not found
        return Response(data={'message': 'Not found!'}, status=status.HTTP_404_NOT_FOUND)

    else:

        # Perhaps bad request data
        return Response(data={'message': 'Error'}, status=status.HTTP_400_BAD_REQUEST)
