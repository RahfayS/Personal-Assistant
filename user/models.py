import uuid
from datetime import datetime

class User:
    def __init__(self, name, email):
        self.id = str(uuid.uuid4())
        self.name = name
        self.email = email
        self.registered_at = datetime.now().strftime("%d/%m/%Y")
        self.encoding = None

    def __repr__(self):
        return f"User(name={self.name}, email={self.email}, encoding={self.encoding})"
