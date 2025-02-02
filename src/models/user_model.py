import bcrypt
from pydantic import BaseModel, validator # , Field, root_validator
from typing import Optional
from datetime import datetime

class UserModel(BaseModel):
    email: str
    password: str
    name: str
    created_at: Optional[datetime] = datetime.utcnow()

    @validator('password')
    def hash_password(cls, v):
        return bcrypt.hashpw(v.encode('utf-8'), bcrypt.gensalt(rounds=10)).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    @validator('email') # check for email uniqueness
    def check_email(cls, v):
        if v in [item.email for item in cls.__instances__]:
            raise ValueError('email address found')

        return v

    __instances__ = []

    def __init__(self, **data):
        super().__init__(**data) # super refer to BaseModel (parent class), init (invoke BaseModel constructor w/o overriding it
        self.__class__.__instances__.append(self)
