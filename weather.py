#! /usr/bin/python3
import requests  # type: ignore[import-untyped]
import json
import sys

import os


class Graph:

    def __init__(self, title: str, category: str,
                 items: list):
        self.title = title
        self.category = category
        self.items = items

    def config(self) -> None:
        config = {
            'graph_title': self.title,
            'graph_category': self.category,
        }

        for item in self.items:
            tag = f"{item['label']}.label"
            title = item['title']
            config[tag] = title

        for key in config:
            print(f'{key} {config[key]}')

    def stats(self, locale: str, api_key: str):
        params = {'key': api_key, 'q': locale}

        r = requests.get(
            url='http://api.weatherapi.com/v1/current.json',
            params=params)

        result = r.text
        decoded = json.loads(result)
        current = decoded['current']

        for item in self.items:
            key = item['key']
            print(f'{key}.value {current[key]}')


def __main__():
    args = sys.argv

    graphs = {
        'temperature': Graph(
            'Temperature', 'weather',
            [{'label': 'temp_c',  'title': 'Degrees Celsius',
              'key': 'temp_c'},
             {'label': 'windchill', 'title': 'Feels like',
              'key': 'windchill_c'}]),
        'pressure': Graph(
            'Air Pressure', 'weather',
            [{'label': 'pressure_mb', 'title': 'Pressure',
              'key': 'pressure_mb'}]),
        'wind_speed': Graph(
            'Wind Speed', 'weather',
            [{'label': 'windspeed', 'title': 'Windspeed in kph',
              'key': 'wind_kph'}]),
        'coverage': Graph(
            'Humidity / Cloud Coverage', 'weather',
            [{'label': 'cloud', 'title': 'Cloud Coverage',
              'key': 'cloud'},
             {'label': 'humidity', 'title': 'Humidity',
              'key': 'humidity'}]),
        'precip': Graph(
            'Precipitation', 'weather',
            [{'label': 'precipitation', 'title': 'Rainfall',
              'key': 'precip_mm'}])

    }

    if 'WEATHER_ACTION' in os.environ:
        graph_type = os.environ['WEATHER_ACTION']
    else:
        graph_type = 'temperature'

    locale = os.environ['WEATHER_LOCALE']
    api_key = os.environ['WEATHERAPI_KEY']

    if len(args) == 2 and args[1] == 'config':
        graphs[graph_type].config()
    else:
        graphs[graph_type].stats(locale, api_key)


__main__()
