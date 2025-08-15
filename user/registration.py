import re
from datetime import datetime
from .models import User
import pickle
import os 

def get_user_info():

    name = str(input('Enter your name: ')).strip().lower()

    # Verifying the users email
    while True:
        email = str(input('Enter your email: ')).strip().lower()
        verified = verify_email(email)
        if verified:
            print('Email Verified')
            break
        else:
            print('Invalid Email format')
        
    return name, email

def check_email(users,email):
    '''
    
    Takes an email and checks to see if it already exists in the data
    
    '''

    user = User()

    emails = [user.email for user.email in users.values()]

    if email in emails:
        print(f'{email} already registered')
        return False
    return True
def verify_email(email):
    '''
    
    Takes an email matches it against a regex pattern to verify if email if of correct format

    Args: 
        email (str): The email address of user
    Returns:
        boolean: True if pattern is valid false if not
    
    '''

    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None


class UserManager:
    def __init__(self, path='user/encodings/encodings.pkl'):
        self.path = path
        self.users = {}
        self.email_to_id = {}
        self.name_to_id = {}

    def register_user(self, name, email):
        if email in self.email_to_id:
            print(f"Email {email} already registered")
            return None
        user = User(name, email)
        self.users[user.id] = user
        self.email_to_id[email] = user.id
        self.name_to_id.setdefault(name, []).append(user.id)
        return user

    def save(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, 'wb') as f:
            print(self.path)
            pickle.dump(self.users, f)


    def load(self):
        if os.path.exists(self.path):
            with open(self.path, 'rb') as f:
                self.users = pickle.load(f)
        return self.users
