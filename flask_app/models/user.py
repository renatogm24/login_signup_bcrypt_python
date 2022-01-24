from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r"^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$])[\w\d@#$]{8,25}$")

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO users (first_name, last_name, email , password, created_at, updated_at ) VALUES ( %(first_name)s , %(last_name)s ,%(email)s ,%(password)s ,NOW() , NOW() );"
        return connectToMySQL('user_bcrypt_schema').query_db( query, data )

    @classmethod
    def get_user_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('user_bcrypt_schema').query_db(query,data)
        if len(results) < 1:
          return False
        return cls(results[0])

    @classmethod
    def exist_mail(cls,data):
        query = "SELECT * FROM users where email = %(email)s;"
        results = connectToMySQL('user_bcrypt_schema').query_db(query,data)
        print(results)
        if len(results) == 0:
          return False
        else:
          return True

    @staticmethod
    def validate_user(user):
      is_valid = True 
      
      if len(user["first_name"])<3:
        flash("First name cant be empty or less than 3 letters","signup")
        is_valid = False
      if len(user["last_name"])<3:
        flash("Last name cant be empty or less than 3 letters","signup")
        is_valid = False
      if not EMAIL_REGEX.match(user["email"]):
        flash("Invalid email address!","signup")
        is_valid = False
      data = {"email":user["email"]}
      if User.exist_mail(data):
        flash("Mail already exist!","signup")
        is_valid = False
      if not PASSWORD_REGEX.match(user["password"]):
        flash("Password needs one Uppercase, Number and Special character, 6 to 12 characters","signup")
        is_valid = False
      if user["password"] != user["repeat_password"]:
        flash("Password does not match","signup")
        is_valid = False
      return is_valid
