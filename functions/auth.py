#!/usr/bin/python3
from argon2 import PasswordHasher


def check_pass(user_pass, passwd):
        """
        password hashing
        """
        ph = PasswordHasher()
        try:
            hash = ph.verify(user_pass ,passwd)
            return True
        except:
            return False