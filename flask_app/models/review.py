from flask_app.config.mysqlconnection import connectToMySQL
from flask import Flask, render_template, request, redirect, flash

class Review:
    db = 'review_proj'
    def __init__( self , data):
        self.id = data['id']
        self.rating = data['rating']
        self.review = data['review']
        self.restaraunt_id = data['restaraunt_id']
        self.user_id = data['user_id']

    @classmethod
    def save(cls, data ):
        query = "INSERT INTO reviews ( rating, review, added, updated, rest_name, user_id) VALUES ( %(rating)s, %(review)s, %(added)s, %(updated)s, %(rest_name)s, %(user_id)s);"
        return connectToMySQL(cls.db).query_db( query, data )
    @staticmethod
    def get_all_user(data):
        query = "SELECT * FROM reviews WHERE user_id = %(user_id)s LIMIT 6;"
        return connectToMySQL(Review.db).query_db( query, data)
    @staticmethod
    def get_all_where_show_attack(data):
        query = "SELECT * FROM restaurants WHERE user_id != %(user_id)s;"
        return connectToMySQL(Review.db).query_db( query, data)
    @staticmethod
    def get_all_restaurant(data):
        query = "SELECT * FROM reviews WHERE restaraunt_id = %(restaraunt_id)s;"
        return connectToMySQL(Review.db).query_db( query, data)
    @staticmethod
    def get_random_6_reviews():
        query = "SELECT * FROM reviews ORDER BY RAND() LIMIT 6;"
        print(query)
        return connectToMySQL(Review.db).query_db( query)
    @staticmethod
    def get_popular_page():
        query = "SELECT * FROM reviews WHERE rating > 3 LIMIT 9 ;"
        print(query)
        return connectToMySQL(Review.db).query_db( query)
