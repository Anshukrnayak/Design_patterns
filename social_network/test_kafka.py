from quixstreams import Application
import requests
import json
import time

app=Application(
    broker_address='localhost:9092',
    loglevel="DEBUG"
)

def setup_producer(value):
    try:
        while True:
            print('push data into kafka :')
            with app.get_producer() as producer:
                producer.produce(
                topic='weather_data',
                key='location',
                value=json.dumps(value)
            )
            print('Successfully push data into kafka : ')
            time.sleep(10)

    except Exception as e:
        print('error : ',e)


def get_weather():
    try:
        response=requests.get(
            'https://api.open-meteo.com/v1/forecast',
            params={
                "latitude":51.1,
                "longitude":-0.11,
                "current":'temperature_2m'
            }
        )
        return response.json()
    except requests.exceptions.RequestException as e:
        return e

response=get_weather()
setup_producer(response)




