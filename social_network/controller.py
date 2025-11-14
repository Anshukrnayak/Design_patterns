import models
import json
from quixstreams import Application

app=Application(
    broker_address='localhost:9092',
    loglevel="DEBUG"
)

class SendToKafka:
    def push(self,topic:str,value,key=None):
        try:
            with app.get_producer() as producer:
                producer.produce(
                    topic=topic,
                    key=key,
                    value=value,
                )
        except Exception as e:
            return json.dumps({'error':e})

class UserProduce(SendToKafka):
    def create_user(self):
        try:
            value=models.User(username='Abhijeet',email='abhijeetkumar3015@gmail',password='#include')
            return  value.response()
        except Exception as e:
            return json.dumps({'error':e})

    def send_to_kafka(self,topic,key=None):
        self.push(topic=topic,value=self.create_user(),key=key)

class ProfileProduce(SendToKafka):
    def create_profile(self):
        try:
            user=models.User(
                username='Abhijeet',
                email='abhijeetkumar3015@gmail',
                password='#include'
            )

            value=models.Profile(
                user=user,
                first_name='Abhijeet',
                last_name='Kumar3015',
                contact=7079840969,
                bio='This is my bio'
            )
            return value.response()
        except Exception as e:
            return json.dumps({'error':e})

    def send_to_kafka(self,topic,key=None):
        self.push(topic=topic,value=self.create_profile(),key=key)


class PostProduce(SendToKafka):
    def create_post(self):
        try:
            user=models.User(
                username='Abhijeet',
                email='abhijeetkumar3015@gmail',
                password='#include'
            )
            value=models.Post(
                user=user,
                title='post',
                content='This is my post',
            )
        except Exception as e:
            return json.dumps({'error':e})

    def send_to_kafka(self,topic,key=None):
        self.push(topic=topic,value=self.create_post(),key=key)


class CommentProduce(SendToKafka):
    def make_comment(self):
        user=models.User(
            username='Abhijeet',
            email='abhijeetkumar3015@gmail',
            password='#include'
        )
        value=models.Comment(
            user=user,
            content='This is my comment',
        )
        return value.response()

    def send_to_kafka(self,topic,key=None):
        self.push(topic=topic,value=self.make_comment(),key=key)