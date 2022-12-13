from flask import current_app as app
from flask_login import current_user

class Review:
    """
    This is just a TEMPLATE for Review, you should change this by adding or 
        replacing new columns, etc. for your design.
    """
    def __init__(self, user_id, product_id, rating, title, content, time_post, product_name, image_url, num_upvotes):
        self.user_id = user_id
        self.product_id = product_id
        self.title = title
        self.content = content
        self.product_name=product_name
        self.image_url=image_url
        self.rating = rating
        self.time_post = time_post
        self.num_upvotes=num_upvotes

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT *
FROM Reviews
WHERE seller_id = :id
''',
                              id=id)
        return Review(*(rows[0])) if rows else None

    @staticmethod
    def get_recent_review(user_id): #change limit to 5 later
        rows = app.db.execute('''
SELECT *
FROM Reviews
WHERE user_id = :user_id 
ORDER BY time_post DESC 
LIMIT 5
''',
                              user_id =user_id)
        return [Review(*row) for row in rows]

    @staticmethod
    def get_user_reviews(user_id):
        rows = app.db.execute('''
SELECT ReviewProduct.user_id, Products.product_id, rating, title, content, time_post, product_name, image_url, num_upvotes
FROM ReviewProduct
LEFT JOIN Products ON ReviewProduct.product_id = Products.product_id
WHERE user_id = :user_id
ORDER BY time_post DESC 
''',
                              user_id =user_id)
        return [Review(*row) for row in rows]

    @staticmethod #get all reviews pertaining to a seller 
    def get_seller_reviews(seller_id):
        rows = app.db.execute('''
SELECT ReviewSeller.user_id, ReviewSeller.seller_id, rating, title, content, time_post
FROM ReviewSeller
WHERE ReviewSeller.seller_id = :seller_id
ORDER BY time_post DESC 
''',
                              seller_id =seller_id)
        return rows
        # return [Review(*row) for row in rows]

    @staticmethod
    def add_review(product_id, rating, title, content, time_post):
        if ";" in title:
            title = title.replace(";","")
        user_id = current_user.id
        rows = app.db.execute("""
    INSERT INTO ReviewProduct(user_id, product_id, rating, title, content, time_post)
    VALUES(:user_id, :product_id, :rating, :title, :content, :time_post)        
    """,
                                    user_id = user_id, product_id= product_id, rating=rating, title=title, content=content, time_post=time_post)
        print("added review successfully!")
        return True

    @staticmethod
    def add_review_seller(seller_id, rating, title, content, time_post):
        user_id = current_user.id
        rows = app.db.execute("""
    INSERT INTO ReviewSeller(user_id, seller_id, rating, title, content, time_post)
    VALUES(:user_id, :seller_id, :rating, :title, :content, :time_post)        
    """,
                                    user_id = user_id, seller_id= seller_id, rating=rating, title=title, content=content, time_post=time_post)
        print("added review successfully!")
        return True


    @staticmethod
    def delete_review(product_id, user_id):   
        print("Review has been deleted")
        rows = app.db.execute("""
    DELETE FROM ReviewProduct
    WHERE product_id = :product_id AND  user_id = :user_id 
    """,
                                    product_id= product_id, user_id=user_id)
        print("deleted product item successfully!")
        return True
    
#     @staticmethod
#     def find_review_to_edit(user_id, product_id, seller_id):
#         rows = app.db.execute('''
# SELECT Reviews.user_id, Products.product_id, seller_id, rating, title, content, time_post, product_name, image_url
# FROM Reviews
# LEFT JOIN Products ON Reviews.product_id = Products.product_id
# WHERE Reviews.product_id = :product_id AND Reviews.seller_id = :seller_id AND  user_id = :user_id 
# ''',
#                                     product_id= product_id, seller_id = seller_id,user_id=user_id)
#         return [Review(*row) for row in rows]

    @staticmethod
    def editReview(user_id, product_id, rating, title, content, time_post):
        if ";" in title:
            title = title.replace(";","")
        try:
            rows = app.db.execute("""
    UPDATE ReviewProduct SET rating = :rating, title = :title, content = :content, time_post = :time_post
    WHERE product_id = :product_id AND user_id = :user_id 
    """,
                                        user_id = user_id, product_id= product_id, rating=rating, title=title, content=content, time_post=time_post)
            print("edited comment successfully!")
            return True
        except Exception as e:
            print(str(e))
            return None

    @staticmethod
    def check_submitted_review(product_id, user_id):
        rows = app.db.execute('''
SELECT *
FROM ReviewProduct, Users
WHERE ReviewProduct.user_id = :user_id AND ReviewProduct.product_id = :product_id
''',
                              product_id=product_id, user_id=user_id)
        return True if rows!=[] else False

    @staticmethod
    def check_submitted_review_seller(seller_id, user_id):
        rows = app.db.execute('''
SELECT *
FROM ReviewSeller, Users
WHERE ReviewSeller.user_id = :user_id AND ReviewSeller.seller_id = :seller_id
''',
                              seller_id=seller_id, user_id=user_id)
        return True if rows!=[] else False

    @staticmethod
    def upvote(user_id, product_id):
        new_num_upvotes = app.db.execute(""" 
SELECT num_upvotes
FROM ReviewProduct 
WHERE user_id = :user_id AND product_id = :product_id 
        """,
                                 user_id=user_id, product_id=product_id)
        rows = app.db.execute("""
UPDATE ReviewProduct SET num_upvotes = :new_num_upvotes+1
WHERE user_id = :user_id AND product_id = :product_id 
""",
                                  user_id=user_id, product_id=product_id, new_num_upvotes = new_num_upvotes[0][0])
        return rows

    @staticmethod
    def downvote(user_id, product_id):
        new_num_upvotes = app.db.execute(""" 
SELECT num_upvotes
FROM ReviewProduct 
WHERE user_id = :user_id AND product_id = :product_id 
        """,
                                 user_id=user_id, product_id=product_id)
        rows = app.db.execute("""
UPDATE ReviewProduct SET num_upvotes = :new_num_upvotes-1
WHERE user_id = :user_id AND product_id = :product_id 
""",
                                  user_id=user_id, product_id=product_id, new_num_upvotes = new_num_upvotes[0][0])
        return rows