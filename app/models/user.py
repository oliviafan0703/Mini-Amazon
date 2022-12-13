from flask_login import UserMixin, current_user
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

from .. import login


class User(UserMixin):
    def __init__(self, id, email, firstname, lastname, mailing_address, balance):
        self.id = id
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.mailing_address = mailing_address
        self.balance = balance

    @staticmethod
    def get_by_auth(email, password):
        if ";" in email:
            email = email.replace(";","")
        if ";" in password:
            password = password.replace(";","")
        
        rows = app.db.execute("""
SELECT passwrd, id, email, firstname, lastname, mailing_address, balance
FROM Users
WHERE email = :email
""",
                              email=email)
        if not rows:  # email not found
            return None
        elif not check_password_hash(rows[0][0], password):
            # incorrect password
            return None
        else:
            return User(*(rows[0][1:]))

    @staticmethod
    def email_exists(email):
        if ";" in email:
            print("hello")
            email = email.replace(";","")
        rows = app.db.execute("""
SELECT email
FROM Users
WHERE email = :email
""",
                              email=email)
        return len(rows) > 0

    @staticmethod
    def register(email, passwrd, firstname, lastname, mailingaddress, checkbox):
        if ";" in email:
            email = email.replace(";","")
        if ";" in passwrd:
            password = password.replace(";","")
        if ";" in firstname:
            firstname = firstname.replace(";","")
        if ";" in lastname:
            lastname = lastname.replace(";","")

        def getPasswordHash(password):
            print(password)
            hashed = generate_password_hash(password)
            print(hashed)
            return hashed
        print("REGISTER")

        def get_sellers(id):
            rows = app.db.execute("""
        SELECT * FROM SELLER 
        WHERE id = id     
        """,
                                        id=id)
            print(rows)

        def insert_seller(id):  
            print("Seller has been inserted")
            rows = app.db.execute("""
        INSERT INTO Seller(id)
        VALUES(:id)        
        """,
                                        id=id)
            print("seller:")
            print(get_sellers(id))
            return True

        try:
            rows = app.db.execute("""
INSERT INTO Users(email, passwrd, firstname, lastname, mailing_address, balance)
VALUES(:email, :passwrd, :firstname, :lastname, :mailing_address, :balance)
RETURNING id
""",
                                  email=email,
                                  passwrd=getPasswordHash(passwrd),
                                  firstname=firstname, 
                                  lastname=lastname, 
                                  mailing_address = mailingaddress,
                                  balance = 0)
            id = rows[0][0]
            if (checkbox):
                insert_seller(id)

            return User.get(id)
        except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            print(str(e))
            return None



    @staticmethod
    @login.user_loader
    def get(id):
        rows = app.db.execute("""
SELECT id, email, firstname, lastname, mailing_address, balance
FROM Users
WHERE id = :id
""",
                              id=id)
        return User(*(rows[0])) if rows else None

    @staticmethod
    def is_seller(id):
        rows = app.db.execute("""
SELECT id
FROM Seller
WHERE id = :id
""",
                              id=id)
        return True if rows!=[] else False

    @staticmethod
    def get_address(id):
        rows = app.db.execute("""
SELECT mailing_address
FROM Users
WHERE id = :id
""",
                              id=id)
        return True if rows!=[] else False

    @staticmethod
    def update_info(firstname, lastname, email, mailing_address):
        if ";" in firstname:
            firstname = firstname.replace(";","")
        if ";" in lastname:
            lastname = lastname.replace(";","")
        if ";" in email:
            email = email.replace(";","")
        try:
            id = current_user.id
            rows = app.db.execute("""
UPDATE Users SET email = :email, firstname = :firstname, lastname = :lastname, mailing_address = :mailing_address
WHERE id = :id
RETURNING id
""",
                                  email=email,firstname=firstname, 
                                  lastname=lastname, id=id, mailing_address=mailing_address)
            id = rows[0][0]
            return User.get(id)
        except Exception as e:
            print(str(e))
            return None

    @staticmethod
    def update_password(new_password):
        if ";" in new_password:
            new_password = new_password.replace(";","")
        hashed = generate_password_hash(new_password)
        print(hashed)
        try:
            id = current_user.id
            rows = app.db.execute("""
UPDATE Users SET passwrd = :passwrd
WHERE id = :id
RETURNING id
""",
                                  id=id, passwrd=hashed)
            id = rows[0][0]
            print("changed password successfully")
            return User.get(id)
        except Exception as e:
            print(str(e))
            return None

    @staticmethod
    def get_balance(id):
        rows = app.db.execute("""
SELECT balance
FROM Users
WHERE id = :id
""",
                              id=id)
        return rows[0][0]


    @staticmethod
    def add_money(balance):
        try:
            id=current_user.id
            b_old=User.get_balance(id)
            print("now balance")
            print(b_old)
            b_new=b_old+balance
            rows = app.db.execute("""
UPDATE Users SET balance = :balance
WHERE id = :id
RETURNING id
""",
                                  balance=b_new, id=id)
            id = rows[0][0]
            return User.get(id)
        except Exception as e:
            print(str(e))
            return None

    @staticmethod
    def withdraw_money(balance):
        try:
            id=current_user.id
            b_old=User.get_balance(id)
            print("withdraw")
            b_new=b_old-balance
            rows = app.db.execute("""
UPDATE Users SET balance = :balance
WHERE id = :id
RETURNING id
""",
                                  balance=b_new, id=id)
            id = rows[0][0]
            return User.get(id)
        except Exception as e:
            print(str(e))
            return None
        
    @staticmethod
    def check_exceed_balance(balance):
        id=current_user.id
        b_old=User.get_balance(id)
        print("checked exceed balance")
        return False if b_old>balance else True


    @staticmethod
    def pay(balance):
        try:
            id=current_user.id
            rows = app.db.execute("""
UPDATE Users SET balance = balance - :balance
WHERE id = :id
RETURNING id
""",
                                  balance=balance, id=id)
            id = rows[0][0]
            return User.get(id)
        except Exception as e:
            print(str(e))
            return None


    @staticmethod
    def credit(balance, sid):
        try:
            rows = app.db.execute("""
UPDATE Users SET balance = balance + :balance
WHERE id = :sid
RETURNING id
""",
                                  balance=balance, sid=sid)
            id = rows[0][0]
            return User.get(id)
        except Exception as e:
            print(str(e))
            return None
