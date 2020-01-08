from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer)
from passlib.apps import custom_app_context as pwd_context


class User:

    def __init__(self, *args, **kwargs):
        self.user_name = kwargs.get('user_name', "")
        self.password_hash = kwargs.get('password', "")
        self.first_name = kwargs.get('first_name', "")
        self.last_name = kwargs.get('last_name', "")

    def get_user_name(self):
        return self.user_name

    def get_password(self):
        return self.password_hash

    def set_password(self, password):
        self.password_hash = password

    def get_first_name(self):
        return self.first_name

    def set_first_name(self, first_name):
        self.first_name = first_name

    def get_last_name(self):
        return self.last_name

    def set_last_name(self, last_name):
        self.last_name = last_name

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, secret_key, expiration=600):
        s = Serializer(secret_key, expires_in=expiration)
        return s.dumps({'id': self.user_name})

    def to_dict(self):
        return {
            "user_name": self.user_name,
            "password_hash": self.password_hash,
            "first_name": self.first_name,
            "last_name": self.last_name
        }