class Employee():
    def __init__(self, db, user):
        self.db = db
        self.user = user

    def login(self):
        print("Hello Employee HERE")