import json
from datetime import datetime
from abc import ABC,abstractmethod,ABCMeta

class BaseModel(metaclass=ABCMeta):
    def __init__(self):
        self._created_at=datetime.time(datetime.now())
        self._updated_at=datetime.time(datetime.now())

    class Meta:
        abstract = True

class User(BaseModel):

    def __init__(self, username, password, email):
        super().__init__()
        self.__username=username
        self.__password=password
        self.__email=email

    def get_username(self):
        return self.__username
    def get_email(self):
        return self.__email
    
    def created_at(self):
        return self._created_at 

    def update_at(self):
        return self._updated_at 

    def response(self):
        data={
            'username':self.__username,
            'email':self.__email,
        }
        return json.dumps(data)

class Profile(BaseModel):
    def __init__(self,user:User,first_name:str,last_name:str,bio:str=None,contact:int=None):
        super().__init__()
        self.__user=user
        self.__first_name=first_name
        self.__last_name=last_name
        self.__bio=bio
        self.__contact=contact
    
    def get_user(self):
        return self.__user 
    
    def get_first_name(self):
        return self.__first_name 

    def get_last_name(self):
        return self.__last_name 

    def get_bio(self):
        return self.__bio 

    def get_contact(self):
        return self.__contact 

    def response(self):
        return json.dumps({
            'user':{
                'username':self.__user.get_username(),
                'email':self.__user.get_email(),
            },
            'first_name':self.__first_name,
            'last_name':self.__last_name,
            'bio':self.__bio,
            'contact':self.__contact,
        })

class Post(BaseModel):
    def __init__(self,user:User,title:str,content:str):
        super().__init__() 

        self.__user=user
        self.__title=title 
        self.__content=content 
        self.__liked=[] 

    def get_user(self):
        return self.__user 
    
    def get_title(self):
        return self.__title

    def get_like_count(self):
        return len(self.__liked) 

    def add_like(self,user:User):
        self.__liked.append(user)

    def response(self):
        data={
            'user':{
                    'username':self.__user.get_username(),
                    'email':self.__user.get_email(),
            },
            'title':self.__title,
            'content':self.__content,
            'like_count':len(self.__liked),
            'created_at':self._created_at
        }
        return json.dumps(data)

class Comment(BaseModel):
    def __init__(self,user:User,content:str):
        super().__init__()
        self.__user=user
        self.__content=content

    def get_user(self):
        return self.__user
    def get_content(self):
        return self.__content

    def response(self):
        return json.dumps({
            'user':{
                'username':self.__user.get_username(),
                'email':self.__user.get_email(),
            },
            'content':self.__content
        })