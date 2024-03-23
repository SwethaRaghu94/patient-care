from flask_app.config.mysqlconnection import connectToMySQL

# from flask_app.models.user import User
from flask_app.models.patient import Patient

from flask import flash

import re

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")


class Provider:

    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
       
        self.patients = []

    @classmethod
    def save(cls, data):
        query = "INSERT INTO providers (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        print(data)
        return connectToMySQL("providers_and_patients").query_db(query, data)

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM providers WHERE email = %(email)s;"
        results = connectToMySQL("providers_and_patients").query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])       

    @staticmethod
    def validate_provider(provider):
        is_valid = True

        if len(provider["first_name"]) < 2:
            flash("First name must be atleast 2 characters")
            is_valid = False
        if len(provider["last_name"]) < 2:
            flash("Last name must be atleast 2 characters")
            is_valid = False
        if len(provider["password"]) < 8:
            flash("Password must be atleast 8 characters")
            is_valid = False
        if not EMAIL_REGEX.match(provider["email"]):
            flash("Email address is not valid!")
            if len(provider["email"]) < 1:
                flash("Email address cannot be blank!")
            is_valid = False
        if provider["password"] != provider["confirm_password"]:
            flash("Your Passwords do not match!")
            is_valid = False
        if provider["email"] in provider:
            flash("Account already exists")
            is_valid = False
        return is_valid
