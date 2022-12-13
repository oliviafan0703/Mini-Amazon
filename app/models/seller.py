from flask import current_app as app


class Seller:
    def __init__(self, user_id, product_uid, rating, time_post):
        self.user_id = user_id
        self.product_uid = product_uid
        self.rating = rating
        self.time_post = time_post

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT user_id, order_id, product_id, order_timestamp
FROM Reviews
WHERE user_id = :user_id
''',
                              user_id=id)
        return Seller(*(rows[0])) if rows else None

    @staticmethod
    def get_recent_comments(user_id):
        rows = app.db.execute('''
SELECT *
FROM Reviews
WHERE user_id = :user_id 
ORDER BY time_post DESC
LIMIT 5
''',
                              user_id=user_id)
        return [Seller(*row) for row in rows]

    @staticmethod
    def update_fulfillment(seller_id, product_id, order_id, new_fulfillment):
        app.db.execute("""
            UPDATE OrderDetails 
            SET fulfill_status = :new_fulfillment 
            WHERE product_id = :product_id AND seller_id = :seller_id AND order_id = :order_id
            """, product_id = product_id, new_fulfillment = new_fulfillment, seller_id = seller_id, order_id = order_id)
        return True