from flask import current_app as app


class OrderP:
    """
    This is just a TEMPLATE for Review, you should change this by adding or 
        replacing new columns, etc. for your design.
    """
    def __init__(self, user_id, order_id, quantity, fulfill_status, order_timestamp, product_name, image_url, price, seller_firstname = "", seller_lastname = "", seller_id = ""):
        self.user_id = user_id
        self.order_id = order_id
        self.quantity = quantity
        self.fulfill_status = fulfill_status
        self.order_timestamp = order_timestamp
        self.product_name = product_name
        self.image_url = image_url
        self.price = price
        self.sellername = seller_firstname + " " + seller_lastname
        self.seller_id = seller_id


    @staticmethod
    def get_ordersP(user_id):
        rows = app.db.execute('''
SELECT O.user_id, O.order_id, OD.quantity, OD.fulfill_status, OD.order_timestamp, P.product_name, P.image_url, I.price
FROM Orders O, OrderDetails OD, Products P, Inventory I
WHERE O.user_id = :user_id and OD.product_id = P.product_id and O.order_id = OD.order_id AND I.product_id = P.product_id and I.seller_id = OD.seller_id
''',
                              user_id = user_id)
        return [OrderP(*row) for row in rows]

    @staticmethod
    def get_order_numbers_by_uid(user_id):
        rows = app.db.execute('''
SELECT Orders.order_id, COUNT(OrderDetails.order_timestamp) as num_products, MIN(OrderDetails.order_timestamp) as timestamp, count(CASE WHEN OrderDetails.fulfill_status THEN 1 END) as num_fulfilled, sum(I.price * OrderDetails.quantity) as total
FROM Orders, OrderDetails, Products P, Inventory I
WHERE Orders.user_id = :user_id AND Orders.order_id = OrderDetails.order_id AND OrderDetails.product_id = P.product_id AND I.product_id = P.product_id and I.seller_id = OrderDetails.seller_id
GROUP BY Orders.order_id
ORDER BY Orders.order_id DESC

''',
                              user_id=user_id,
                       )
        return rows

    
    @staticmethod
    def is_order_fulfilled(order_id):
        rows = app.db.execute('''
SELECT Orders.order_id, COUNT(OrderDetails.order_timestamp) as num_entries, MIN(OrderDetails.order_timestamp) as timestamp, count(CASE WHEN OrderDetails.fulfill_status THEN 1 END) as num_fulfilled
FROM Orders, OrderDetails
WHERE Orders.order_id = :order_id AND Orders.order_id = OrderDetails.order_id
GROUP BY Orders.order_id

''',
                              order_id=order_id,
                       )

        num_entries = rows[0].num_entries
        num_fulfilled = rows[0].num_fulfilled
        return num_entries == num_fulfilled

    @staticmethod
    def get_orders_by_order_id(order_id):
        rows = app.db.execute('''
SELECT O.user_id, O.order_id, OD.quantity, OD.fulfill_status, OD.order_timestamp, P.product_name, P.image_url, I.price, Users.firstname as seller_firstname, Users.lastname as seller_lastname, OD.seller_id
FROM Orders O, OrderDetails OD, Products P, Seller, Users, Inventory I
WHERE O.order_id = :order_id and OD.product_id = P.product_id and O.order_id = OD.order_id and OD.seller_id = Seller.id and Seller.id = Users.id AND I.product_id = P.product_id and I.seller_id = OD.seller_id
''',
                              order_id = order_id)
        return [OrderP(*row) for row in rows]
    def check_ordered_product(product_id, user_id):
        rows = app.db.execute('''
SELECT *
FROM Orders O, OrderDetails OD
WHERE O.user_id = :user_id and OD.product_id = :product_id and O.order_id = OD.order_id
''',
                              user_id = user_id, product_id = product_id)
        return True if rows!=[] else False

    @staticmethod
    def check_ordered_seller(seller_id, user_id):
        rows = app.db.execute('''
SELECT *
FROM Orders O, OrderDetails OD
WHERE OD.seller_id = :seller_id and O.user_id  = :user_id and O.order_id = OD.order_id
''',
                              seller_id = seller_id, user_id = user_id)
        return True if rows!=[] else False

    @staticmethod
    def get_order_sold_by_seller(product_id):
        rows = app.db.execute('''
SELECT Users.id as seller_id, SUM(quantity) AS total_quantity, Users.firstname, Users.lastname
FROM OrderDetails, Users
WHERE product_id = :product_id AND Users.id = seller_id
GROUP BY Users.id
''',
                              product_id = product_id)
        return rows
