from flask import current_app as app
from flask_login import current_user


class Inventory:
    def __init__(self, seller_id, product_id, product_name, quantity, price, product_description):
        self.seller_id = seller_id
        self.product_id = product_id
        self.product_name = product_name
        self.price = price
        self.quantity = quantity
        self.product_description = product_description
        

    @staticmethod
    def get(seller_id):
        """ Get all products for sale by this user
        """
        rows = app.db.execute('''
        SELECT seller_id, Inventory.product_id, product_name, Inventory.quantity, price
        FROM Inventory 
        LEFT JOIN Products ON Inventory.product_id = Products.product_id
        WHERE seller_id = :seller_id
            ''', seller_id=seller_id)
        return rows

    @staticmethod
    def add_product(product_id, quantity, price, product_description):
        """Add product to inventory
        """
        seller_id = current_user.id
        app.db.execute("""
            INSERT INTO Inventory(product_id, quantity, seller_id, product_description, price)
            VALUES(:product_id, :quantity, :seller_id, :product_description, :price)
            """,product_id = product_id, quantity = quantity, price=price, seller_id=seller_id, product_description=product_description)
        return None

    @staticmethod
    def edit_product(product_id, quantity, price, product_description):
        app.db.execute("""
            UPDATE Inventory 
            SET quantity = :quantity, price = :price, product_description = :product_description
            WHERE product_id = :product_id AND seller_id = :seller_id
            """, product_id = product_id, quantity = quantity, seller_id = current_user.id, price = price, product_description = product_description)
        return True
   

    @staticmethod
    def remove_product(product_id):
        """Remove product from inventory
        """
        seller_id = current_user.id
        app.db.execute("""
            DELETE FROM Inventory
            WHERE seller_id = :seller_id AND product_id = :product_id
            """,product_id = product_id, seller_id=seller_id)
        return None