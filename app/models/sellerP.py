from flask import current_app as app


class SellerP:
    def __init__(self, seller_id, product_uid, quantity, order_id, fulfill_status, order_timestamp, buyer_id, buyer_address):
        self.seller_id = seller_id
        self.product_uid = product_uid
        self.quantity = quantity
        self.order_id = order_id
        self.fulfill_status = fulfill_status
        self.order_timestamp = order_timestamp
        self.buyer_id = buyer_id
        self.buyer_address = buyer_address
    


    @staticmethod
    def get_order_history(seller_id):
        rows = app.db.execute('''
SELECT seller_id, product_id, quantity, O.order_id, fulfill_status, 
       DATE(order_timestamp),  
       O.user_id, U.mailing_address
FROM Orders O, OrderDetails OD, Users U
WHERE OD.seller_id = :seller_id AND O.order_id = OD.order_id AND O.user_id = U.id
ORDER BY OD.order_timestamp DESC
''',
                              seller_id=seller_id)


        
        return [SellerP(*row) for row in rows]

    @staticmethod
    def get_created_products(seller_id):
        rows = app.db.execute('''
SELECT P.product_id, image_url, product_name, category_name, quantity, product_description, price
FROM Products P, Inventory I
WHERE owner_id = :seller_id AND I.product_id = P.product_id
''',
                              seller_id=seller_id)
        
        return rows
  

       

    


    