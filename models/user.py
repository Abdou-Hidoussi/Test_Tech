#!/usr/bin/python3
from uuid import uuid4
from argon2 import PasswordHasher
from functions.db import save_user_to_database

class User(object):
    def __init__(self, first, last, email, passwd, fav=[]):
        """
        class initialization 
        """    
        self.uid = str(uuid4())
        self.first_name = first
        self.last_name = last
        self.email = email
        self.password = self.hash_pass(passwd)
        self.favorites = fav

    def hash_pass(self, passwd):
        """
        password hashing
        """
        ph = PasswordHasher()
        hash = ph.hash(passwd)
        return hash

    def save(self):
        return save_user_to_database(self.__dict__)