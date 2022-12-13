from flask import current_app as app
from flask_login import current_user


class Order:
    """
    This is just a TEMPLATE for Review, you should change this by adding or 
        replacing new columns, etc. for your design.
    """
    def __init__(self, user_id, order_id, quantity, fulfill_status, order_timestamp, product_id):
        self.user_id = user_id
        self.order_id = order_id
        self.quantity = quantity
        self.fulfill_status = fulfill_status
        self.order_timestamp = order_timestamp
        self.product_id = product_id

    @staticmethod
    def create_order():   
        #returns an order id of the created order 
        rows = app.db.execute("""
    INSERT INTO Orders(user_id)
    VALUES(:u_id)        
    RETURNING order_id
    """,
                                    u_id=current_user.id)
        print("created order")
        return rows[0][0]

    @staticmethod
    def add_to_order(order_id, pid, sid, quantity): #unfufilled
            #returns an order id of the created order 
        rows = app.db.execute("""
    INSERT INTO OrderDetails(order_id, quantity, fulfill_status, product_id, seller_id)
    VALUES(:order_id, :quantity, :fulfill_status, :pid, :sid)        
    RETURNING order_id
    """,
                                    order_id=order_id, 
                                    quantity = quantity,
                                    pid = pid,
                                    sid = sid,
                                    fulfill_status = False
                                    )
        print("created order item")
        return rows[0][0]


    @staticmethod
    def get_all_by_uid_since(user_id, since):
        rows = app.db.execute('''
SELECT Orders.user_id, Orders.order_id, OrderDetails.quantity, OrderDetails.fulfill_status, OrderDetails.order_timestamp, OrderDetails.product_id
FROM Orders, OrderDetails
WHERE Orders.user_id = :user_id AND Orders.order_id = OrderDetails.order_id
AND OrderDetails.order_timestamp >= :since
ORDER BY OrderDetails.order_timestamp DESC
''',
                              user_id=user_id,
                              since=since)
        return [Order(*row) for row in rows]



    @staticmethod
    def get_order_numbers_by_uid(user_id, since):
        rows = app.db.execute('''
SELECT UNIQUE Orders.order_id, OrderDetails.order_timestamp
FROM Orders, OrderDetails
WHERE Orders.user_id = :user_id AND Orders.order_id = OrderDetails.order_id
AND OrderDetails.order_timestamp >= :since
ORDER BY OrderDetails.order_timestamp DESC
''',
                              user_id=user_id,
                              since=since)
        return [Order(*row) for row in rows]



