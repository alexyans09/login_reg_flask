from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
import re

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")
PASSWORD_REGEX = re.compile(r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$")

class User:
    DB = "vinyl_schema"

    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @staticmethod
    def validate_register(user):
        is_valid = True
        if len(user["first_name"].strip()) == 0:
            flash("First Name required", "registter")
            is_valid = False
        elif len(user["first_name"].strip()) < 2:
            flash("First Name must be at least 2 characters", "register")
            is_valid = False

        if len(user["last_name"].strip()) == 0:
            flash("Last Name required", "registter")
            is_valid = False
        elif len(user["last_name"].strip()) < 2:
            flash("Last Name must be at least 2 characters", "register")
            is_valid = False

        if len(user["email"].strip()) == 0:
            flash("invalid Email Address", "registter")
            is_valid = False
        elif not EMAIL_REGEX.match(user["email"]):
            flash("Email Invalid", "register")
            is_valid = False

        if len(user["password"].strip()) == 0:
            flash("Password required", "register")
            is_valid = False
        elif len(user["password"].strip()) < 8:
            flash("password must be at least eight character", "register")
            is_valid = False
        elif not PASSWORD_REGEX.match(user["password"].strip()):
            flash(
                "Password must contain at least 1 capital letter, 1 number and 1 special character (!@#$)",
                "register",
            )
            is_valid = False
        elif user["password"] != user["password_confirm"]:
            flash("Passwords do not match", "register")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_login(user):
        """This method validates the login form."""
        is_valid = True
        if len(user["email"].strip()) == 0:
            flash("Email Address is required", "login")
            is_valid = False
        elif not EMAIL_REGEX.match(user["email"]):
            flash("Invalid Email Address", "login")
            is_valid
        if len(user["password"].strip()) == 0:
            flash("Please Enter Password.", "login")
            is_valid
        elif len(user["password"].strip()) < 8:
            flash("Password must be at least eight characters", "login")
            is_valid = False
        return is_valid

    @classmethod
    def register(cls, user_data):
        """This method create a new user in the database."""
        query = """INSERT INTO users 
        (first_name, last_name, email, password,
        created_at, updated_at) VALUES ( %(first_name)s, %(last_name)s, %(email)s,
        %(password)s, NOW(), NOW());"""

        user_id = connectToMySQL(cls.DB).query_db(query, user_data)
        return user_id

    @classmethod
    def find_by_email(cls, email):
        """This method finds a user by email."""
        query = "SELECT * FROM users WHERE email = %(email)s;"
        data = {"email": email}
        list_of_dicts = connectToMySQL(cls.DB).query_db(query, data)
        if len(list_of_dicts) == 0:
            return None
        user = User(list_of_dicts[0])
        return user

    @classmethod
    def find_by_user_id(cls, user_id):
        query = "SELECT * FROM users WHERE id = %(user_id)s;"
        data = {"user_id": user_id}
        list_of_dicts = connectToMySQL(cls.DB).query_db(query, data)
        if len(list_of_dicts) == 0:
            return None
        user = User(list_of_dicts[0])
        return user
