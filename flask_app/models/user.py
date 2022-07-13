from flask_app.config.mysqlconnection import connectToMySQL
from flask import Flask, render_template, request, redirect, flash
import re
from flask_bcrypt import Bcrypt

class User:
    db = 'review_proj'
    def __init__( self , data):
        self.id = data['id']
        self.email = data['email']
        self.fname = data['fname']
        self.lname = data['lname']
        self.password = data['password']
        self.username = data['username']
        self.added = data['added']

    @classmethod
    def save(cls, data ):
        query = "INSERT INTO users ( fname, lname, email, password) VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(cls.db).query_db( query, data )
    @staticmethod
    def update_one_password(data):
        query = "UPDATE users SET password = %(new_pass)s WHERE id = %(id)s;"
        print(query)
        return connectToMySQL(User.db).query_db( query, data)
    @staticmethod
    def verf_email_original(data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        verf = False
        print(query)
        x = connectToMySQL(User.db).query_db( query, data )
        print(x)
        print(type(x))
        try:
            if len(x) > 0:
                verf = True
        except TypeError:
            return verf
        return verf

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(User.db).query_db(query,data)
        
        try:
            if len(result) < 1:
                return False
        except TypeError:
            return False
        return cls(result[0])
    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        return connectToMySQL(User.db).query_db(query,data)
        

    @staticmethod
    def get_one(data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        return connectToMySQL(User.db).query_db( query, data)
    @staticmethod
    def validate_creds(data):
        validate = True
        if len(data['first_name']) < 3 and len(data['first_name']) != 0:
            validate = False
            flash('First Name needs to be greater than 3 characters', 'first_name')
        if data['first_name'] == '':
            validate = False
            flash('First Name needs to be submitted', 'first_name')
        if not data['first_name'].isalpha():
            validate = False
            flash('First Name needs to be only alphabet characters', 'first_name')
        if len(data['last_name']) < 3 and len(data['last_name']) != 0:
            validate = False
            flash('Last Name needs to be greater than 3 characters', 'last_name')
        if data['last_name'] == '':
            validate = False
            flash('Last Name needs to be submitted', 'last_name')
        if not data['last_name'].isalpha():
            validate = False
            flash('Last Name needs to be only alphabet characters', 'last_name')
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!", 'email')
            validate = False
        if data['password'] != data['conf_password']:
            validate = False
            flash('passwords not matching', 'password')
        if len(data['password']) < 8:
            validate = False
            flash('password needs to be greater than 8 characters', 'password')
        if User.verf_email_original({'email':data['email']}):
            validate = False
            flash('email is aready used', 'email')
        return validate