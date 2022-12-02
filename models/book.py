#!/usr/bin/python3
from uuid import uuid4
from functions.db import save_book_to_database


class Book(object):
    def __init__(self, *args):
        """
        class initialization 
        """    
        at_list = ["title", "author", "publish_date", "description", "created_by"]
        self.isbn = str(uuid4())

        if len(args) != 0:
            for k, v in args[0].items():
                if k in at_list:
                    self.__dict__[k] = v
        
    def save(self):
        return save_book_to_database(self.__dict__)