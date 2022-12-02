#!/usr/bin/python3
"""
    creates a Flask web application
    that provides a REST API for a database of users.
    and regiter the blueprints for the auth and admin modules.
"""
from flask import Flask, request, url_for, redirect, render_template, jsonify
from models.user import User
from models.book import Book
import jwt
import redis
from datetime import timedelta
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from functions.auth import check_pass
from functions.db import check_email, get_user, get_book, find_all_book, find_one_book, find_one_fav



ACCESS_EXPIRES = timedelta(hours=1)

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "secret" 
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES
jwt = JWTManager(app)


jwt_redis_blocklist = redis.StrictRedis(
    host="localhost", port=6379, db=0, decode_responses=True
)


# Callback function to check if a JWT exists in the redis blocklist
@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    """
    Check if token is revpoked

    Return : token or None
    """
    jti = jwt_payload["jti"]
    token_in_redis = jwt_redis_blocklist.get(jti)
    return token_in_redis is not None

@app.route('/register', methods=["POST"])
def register():
    """
    Endpoint to register a new user.
    
    Return: string
    """
    for x in request.form:
        if x == "":
            return jsonify("Plase filla all fields")
    if check_email(request.form["email"]):
        return jsonify("Email already exist")
    try:
        email = request.form["email"]
        fn = request.form["first_name"]
        ln = request.form["last_name"]
        pas = request.form["password"]
    except:
        return jsonify("Please provide email, first_name, last_name, password")
    new_user = User(email=email, first=fn, last=ln, passwd=pas)
    new_user.save()
    return jsonify({"User created successfuly" : new_user.__dict__})

@app.route('/login', methods=["POST"])
def login():
    """
    Endpoint to login a user.
    
    Return: string
    """
 
    auth = request.form
    if not auth or not auth.get('email') or not auth.get('password'):
        return jsonify("Plase provide an email and password")
    user = get_user(auth["email"])
    if user == None:
        return jsonify("No such user")
    if not check_pass(user["password"], auth["password"]):
        return jsonify("Wrong password")
    
    access_token = create_access_token(identity=user["uid"])
    resp = jsonify(access_token)
    resp.set_cookie('user_id', user["uid"])
    return resp

@app.route("/logout", methods=["DELETE"])
@jwt_required()
def logout():
    """
    Endpoint to logout user

    Return : string
    """
    jti = get_jwt()["jti"]
    jwt_redis_blocklist.set(jti, "", ex=ACCESS_EXPIRES)
    return jsonify(msg="Access token revoked")



@app.route("/create_book", methods=["POST"])
@jwt_required()
def create_book():
    """
    Endpoint to create a Book.
    
    Return: string
    """
    user_id = request.cookies.get('user_id')
    dic = {}
    for x in request.form:
        dic[x] = request.form[x]
    dic["created_by"] = user_id
    new_book = Book(dic)
    new_book.save()
    return jsonify("Book Created")


@app.route("/edit_book/<id>", methods=["POST"])
@jwt_required()
def edit_book(id):
    """
    Endpoint to edit a Book.
    
    Return: string
    """
    user_id = request.cookies.get('user_id')
    find = get_book(id)
    if find == None:
        return jsonify("book not found")
    if user_id != find["create_by"]:
        return  jsonify("you are not this books creator")
    dic = {}
    for x in request.form:
        dic[x] = request.form[x]
    try:
        find.update_book(dic)
    except:
        return jsonify("somthing went wrong")
    return jsonify("book updated successfuly")


@app.route("/delete_book/<id>", methods=["DELETES"])
@jwt_required()
def delete_book(id):
    """
    Endpoint to delete a Book.
    
    Return: string
    """
    user_id = request.cookies.get('user_id')
    find = get_book()
    if find == None:
        return jsonify("book not found")
    if user_id != find["create_by"]:
        return  jsonify("you are not this books creator")
    #try:
    #    find.delete(id)
    #except:
    #    return jsonify("somthing went wrong")
    #return jsonify("book deleted successfuly")


@app.route("/book_list", methods=["GET"])
def book_list():
    find = []
    find = find_all_book()
    return jsonify(find)

@app.route("/book/<id>", methods=["GET"])
def book(id):
    find = {}
    find = find_one_book(id)
    return jsonify(find)


@app.route("/add_fav/<id>", methods=["POST"])
@jwt_required()
def add_fav(id):
    user_id = request.cookies.get('user_id')
    find = {}
    #find = find_one({"id" : user_id})
    #find.fav.append(id)
    #find.update()
    return jsonify(find)

@app.route("/show_fav/<id>", methods=["GET"])
#@jwt_required()
def show_fav(id):
    find = {}
    find = find_one_fav(id)
    return jsonify(find)

@app.route("/remove_fav/<id>", methods=["POST"])
@jwt_required()
def remove_fav(id):
    user_id = request.cookies.get('user_id')
    find = {}
    #find = find_one({"id" : user_id})
    #find.fav.pop(id)
    #find.update()
    return jsonify(find)

if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)