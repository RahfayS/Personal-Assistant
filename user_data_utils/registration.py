import re
from datetime import datetime
import uuid
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

class User:
    def __init__(self, name, email):
        self.id = str(uuid.uuid4())
        self.name = name
        self.email = email
        self.registered_at = datetime.now().strftime("%d/%m/%Y")
        self.encoding = None
    def __repr__(self):
        return f'(name = {self.name}, email = {self.email}, encoding = {self.encoding.shape} )'    

class userManager:
    def __init__(self):
        self.users = {}
        self.email_to_id = {}
        self.name_to_id = {}

    def register_user(self, name, email):        
        if email in self.email_to_id:
            print(f'Email {email} already registered')
            return None
        
        user = User(name, email)
        self.users[user.id] = user
        self.email_to_id[email] = user.id
        self.name_to_id.setdefault(name, []).append(user.id)
        return user

    def __repr__(self):
        return f"UserManager({len(self.users)} users)"

    def save_users(self, path='./user_data_utils/encodings.pkl'):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        try:
            with open(path, 'wb') as f:
                pickle.dump(self.users, f)
            print(f'[INFO] Users successfully saved to {path}')
        except Exception as e:
            print(f'[ERROR] Failed to save users: {e}')

    def load_users(self, path='./user_data_utils/encodings.pkl'):
        if os.path.exists(path):
            try:
                with open(path, 'rb') as f:
                    self.users = pickle.load(f)
                print(f'[INFO] Loaded {len(self.users)} users from {path}')
            except Exception as e:
                print(f'[ERROR] Failed to load users: {e}')
                self.users = {}
        else:
            print(f'[WARN] No user file found at {path}')
            self.users = {}
        return self.users
