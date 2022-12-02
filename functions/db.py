
import firebase_admin
from firebase_admin import firestore



import firebase_admin
from firebase_admin import credentials

import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

cred = credentials.Certificate(str(dir_path) + "/key.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

def save_user_to_database(obj):
    res = db.collection(u'user').document(obj["uid"]).set(obj)
    return res

def save_book_to_database(obj):
    res = db.collection(u'book').document(obj["isbn"]).set(obj)
    return res

def check_email(email):
    docs = db.collection(u'user').where(u'email', u'==', email).stream()

    for doc in docs:
        if doc:
            return True
    return False

def get_user(email):
    docs = db.collection(u'user').where(u'email', u'==', email).stream()

    for doc in docs:
        if doc:
            return doc.to_dict()
    return None

def get_book(id):
    docs = db.collection(u'book').where(u'isbn', u'==', id).stream()

    for doc in docs:
        if doc:
            return doc.to_dict()
    return None    

def update_book():
    return

def find_all_book():
    docs = db.collection(u'book').stream()
    new = []
    for doc in docs:
        new.append(doc.to_dict())
    return new

def find_one_book(id):
    docs = db.collection(u'book').where(u'isbn', u'==', id).stream()

    for doc in docs:
        if doc:
            return doc.to_dict()
    return None    

def find_one_fav(id):
    docs = db.collection(u'user').where(u'uid', u'==', id).stream()

    for doc in docs:
        if doc:
            return doc.to_dict()["favorites"]
    return None    