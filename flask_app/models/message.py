from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

from flask_app.models import user
from datetime import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r"^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$])[\w\d@#$]{8,25}$")

class Message:
    def __init__( self , data ):
        self.id = data['id']
        self.user_from = data['user_from']
        self.user_to = data['user_to']
        self.text = data['text']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.time_ago = data['time_ago']

    @classmethod
    def save(cls, data ):
        query = "INSERT INTO messages (user_from_id, user_to_id, text , created_at, updated_at ) VALUES ( %(user_from_id)s , %(user_to_id)s ,%(text)s ,NOW() , NOW() );"
        return connectToMySQL('dojo_chat').query_db( query, data )

    @classmethod
    def get_messages_received(cls,data):
        query = "SELECT * FROM messages WHERE messages.user_to_id = %(id)s order by messages.created_at DESC;"
        results = connectToMySQL('dojo_chat').query_db(query,data)
        messages = []
        if len(results) < 1:
          return False
        for message in results:

          time_between = (datetime.now() - message["created_at"])
          diff_in_seconds = time_between.total_seconds()
          time_ago = ""
          if diff_in_seconds < 60:
            time = int(divmod(diff_in_seconds , 1)[0])
            time_ago = f"{time} seconds ago"
          if diff_in_seconds >= 60 and diff_in_seconds <3600:
            time = int(divmod(diff_in_seconds , 60)[0])
            time_ago = f"{time} minutes ago"
          if diff_in_seconds >= 3600 and diff_in_seconds<86400:
            time = int(divmod(diff_in_seconds , 3600)[0])
            time_ago = f"{time} hours ago"
          if diff_in_seconds >= 86400:
            time = int(divmod(diff_in_seconds , 86400)[0])
            time_ago = f"{time} days ago"

          dataMsg = {
            "id": message["id"],
            "user_from" : user.User.get_user_by_id({"id":message["user_from_id"]}),
            "user_to" : message["user_to_id"],
            "text" : message["text"],
            "created_at" : message["created_at"],
            "updated_at" : message["updated_at"],
            "time_ago" : time_ago,
          }
          messages.append(cls(dataMsg))
        return messages

    @classmethod
    def get_messages_sent(cls,data):
        query = "SELECT count(messages.id) as count FROM messages WHERE messages.user_from_id = %(id)s;"
        result = connectToMySQL('dojo_chat').query_db(query,data)
        return result[0]["count"]

    @classmethod
    def get_message_recipient(cls,data):
        query = "SELECT messages.user_to_id as recipient FROM messages WHERE messages.id = %(id)s;"
        result = connectToMySQL('dojo_chat').query_db(query,data)
        return result[0]["recipient"]

    @classmethod
    def delete_message(cls,data):
        query = "DELETE FROM messages where id = %(id)s;"
        connectToMySQL('dojo_chat').query_db(query,data)

    @staticmethod
    def validate_message(message):
      is_valid = True 
      if len(message["text"])<5:
        flash("Text less than 3 letters","message")
        is_valid = False
      return is_valid


