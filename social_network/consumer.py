from quixstreams import Application
import requests
import json
import time

def setup_consumer():
    app=Application(
        broker_address='localhost:9092',
        loglevel='DEBUG',
        consumer_group='weather_data'
    )
    try:
        with app.get_consumer() as consumer:
            consumer.subscribe(["weather_data"])
            while True:
                try:
                    message=consumer.poll(1)
                    print('running consumer application.... ')
                    if message is None:
                        print('Consumer is waiting for response : ')
                    print(message.value())
                except Exception as e:
                    print(f'error: {e} ')
                time.sleep(10)

    except Exception as e:
        print('error : ',e)

setup_consumer()


