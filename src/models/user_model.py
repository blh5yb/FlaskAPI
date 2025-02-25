import bcrypt
from flask import request
from pydantic import BaseModel, validator, ValidationError # , Field, root_validator
from typing import Optional
from datetime import datetime
from db import db
from pymongo.collection import Collection


class UserModel(BaseModel):
    email: str
    password: str
    name: Optional[str]
    created_at: Optional[datetime] = datetime.utcnow()

    @validator('password')
    def hash_password(cls, v):
        print('path', request.path)
        if request.path == '/flask-demo/api/register': # or update user?
            hashed_pass = bcrypt.hashpw(v.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            return hashed_pass
        return v

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
