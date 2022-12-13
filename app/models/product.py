from flask import current_app as app, jsonify
from flask_login import current_user

class Product:
    def __init__(self, product_id, image_url, product_name, category_name, owner_id):
        self.product_id = product_id
        self.image_url = image_url
        self.product_name = product_name
        # self.product_description = product_description
        # self.price = price
        # self.quantity = quantity
        self.category_name = category_name
        self.owner_id = owner_id


    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT *
FROM Products
WHERE product_id = :id
''',
                              id=id)
        return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_k_products(k):
        rows = app.db.execute(f'''
SELECT * 
FROM Products
ORDER BY price DESC
LIMIT {k}
'''
                              )
        return [Product(*row) for row in rows]

    @staticmethod
    def get_user_cart(u_id):
        rows = app.db.execute('''
SELECT P.product_id, P.image_url, P.product_name, I.product_description, I.price, C.quantity, P.category_name, C.seller_id
FROM CartItems C, Products P, Inventory I
WHERE P.product_id = C.product_ID AND C.u_id = :u_id AND C.seller_id = I.seller_id AND I.product_id = P.product_id
''',
                              u_id=u_id)
        return rows

    @staticmethod
    def get_seller_inventory_2(u_id):
        rows = app.db.execute('''
SELECT Products.product_id, Products.image_url, Products.product_name, Products.category_name, Seller.id
FROM Seller, Inventory, Products
WHERE Seller.id = Inventory.seller_id AND Seller.id = :u_id AND Inventory.product_id = Products.product_id
''',
                              u_id=u_id)
        return rows

    @staticmethod
    def get_sellers_by_product(product_id):
        rows = app.db.execute('''
SELECT Users.firstname, Users.lastname, Inventory.quantity, Inventory.product_description, Seller.id, Inventory.price
FROM User, Seller, Inventory, Users
WHERE Users.id = Seller.id AND Seller.id = Inventory.seller_id AND  Inventory.product_id = :product_id
''',
                              product_id=product_id)
        # data = []
        # for row in rows:
        #     data.append(row)

        # return data

        return rows
    


    @staticmethod
    def get_reviews_by_product(product_id):
        rows = app.db.execute('''
SELECT Users.firstname, Users.lastname, ReviewProduct.rating, ReviewProduct.content, ReviewProduct.time_post, ReviewProduct.title, ReviewProduct.num_upvotes, ReviewProduct.product_id, ReviewProduct.user_id
FROM ReviewProduct, Users
WHERE ReviewProduct.user_id = Users.id AND ReviewProduct.product_id = :product_id
ORDER BY time_post desc
''',
                              product_id=product_id)
        # data = []
        # for row in rows:
        #     data.append(row)

        # return data
        return rows
    
    @staticmethod
    def get_products( search_key, category_key, sort_key, show_available, page = 1, limit = 10, available=True,):
        if ";" in search_key:
            search_key = search_key.replace(";", "")
        if ";" in category_key:
            category_key = category_key.replace(";", "")
        if ";" in sort_key:
            sort_key = sort_key.replace(";", "")

        def categoryquery(category_key):
            if ";" in category_key:
                category_key = category_key.replace(";", "")
            if category_key == "all":
                return ""
            else:
                return f"AND category_name = '{category_key}'"
            
        sort_map = {

            "id_asc":"product_id",
            "price_asc":"price",
            "price_desc":"price DESC"
        }
        # print("showavaialble")
        # print(show_available)
        # def available_only(show_available):
        #     if show_available == True:
        #         return f"HAVING MIN(I.quantity)>0"
        #     else:
        #         print('not showing available')
        #         return ""

        #         # {available_only(show_available)}

        rows = app.db.execute(f'''
SELECT P.product_id, image_url, product_name, category_name, MIN(I.price) as price
FROM Products P, Inventory I
WHERE (UPPER(product_name) LIKE UPPER('%{search_key}%') OR UPPER(product_description) LIKE UPPER('%{search_key}%'))  {categoryquery(category_key)} AND P.product_id = I.product_id 
GROUP BY P.product_id
ORDER BY {sort_map[sort_key]}
LIMIT { limit}
OFFSET { limit*(page-1)}

''',
                             )
        print(rows)
        return rows
        # return [Product(*row) for row in rows]
    
    @staticmethod
    def get_category_names():
        rows = app.db.execute(f'''
SELECT DISTINCT category_name
FROM Products
ORDER BY category_name
''',
                             )

        categories = []
        for row in rows:
            categories.append(row[0])

        return categories
    @staticmethod
    def get_total_products(search_key, page = 1, limit = 10, available=True):
        if ";" in search_key:
            search_key = search_key.replace(";", "")
        rows = app.db.execute(f'''
SELECT count(product_id)
FROM Products
WHERE product_name LIKE '%{search_key}%'
''',
                             )
        return rows[0][0]


    def add_cart_item(quantity, product_id, seller_id, u_id):   
        rows = app.db.execute("""
    INSERT INTO CartItems(quantity, product_id, seller_id, u_id)
    VALUES(:quantity, :product_id, :seller_id, :u_id)        
    """,
                                    quantity = quantity, product_id= product_id, seller_id = seller_id,u_id=u_id)
        print("added product item successfully!")
        return True


    @staticmethod
    def update_cart_item_qty(sid, pid, uid, quantity):
        try:
            rows = app.db.execute("""
UPDATE CartItems SET quantity = :quantity
WHERE product_id = :pid AND seller_id = :sid AND u_id = :uid
RETURNING product_id, seller_id
""",
                                  quantity=quantity, pid=pid, uid = uid, sid=sid)
            ret = rows[0][0]
            return ret
        except Exception as e:
            print(str(e))
            return None

    @staticmethod
    def get_seller_inventory(sid, pid):
        try:
            rows = app.db.execute("""
SELECT quantity FROM Inventory
WHERE product_id = :pid AND seller_id = :sid 
""",
                                   pid=pid, sid=sid)
            ret = rows[0][0]
            return ret
        except Exception as e:
            print(str(e))
            return None


    @staticmethod
    def remove_from_inventory(sid, pid, quantity):
        try:
            rows = app.db.execute("""
UPDATE Inventory SET quantity = quantity - :quantity
WHERE product_id = :pid AND seller_id = :sid 
RETURNING quantity
""",
                                   quantity = quantity, pid=pid, sid=sid)
            ret = rows[0][0]
            return ret
        except Exception as e:
            print(str(e))
            return None

    def remove_cart_item(product_id, seller_id, u_id):   
        print("Cart Item has been deleted")
        print(f'seller id: {seller_id}')
        rows = app.db.execute("""
    DELETE FROM CartItems 
    WHERE product_id = :product_id AND seller_id = :seller_id AND u_id = :u_id        
    """,
                                    product_id= product_id, seller_id = seller_id,u_id=u_id)
        print("deleted product item successfully!")
        return True

    @staticmethod
    def create_product(product_name, image_url, price, product_description, category_name, quantity):
        if ";" in product_name:
            product_name = product_name.replace(";","")
        if ";" in category_name:
            category_name = category_name.replace(";","")
        next_id = app.db.execute("""
SELECT MAX(product_id)+1 FROM Products
                """)
        owner_id = current_user.id
        row = app.db.execute("""
INSERT INTO Products(product_id, image_url, product_name, category_name, owner_id)
VALUES(:new_product_id, :image_url, :product_name, :category_name, :owner_id)
RETURNING product_id
""",
        new_product_id = next_id[0][0], image_url = image_url, product_name = product_name, category_name = category_name, owner_id = owner_id)
        seller_id = current_user.id
        row2 = app.db.execute("""
INSERT INTO Inventory(product_id, quantity, seller_id, product_description, price)
VALUES(:product_id, :quantity, :seller_id, :product_description, :price)
RETURNING product_id
""",
        product_id = next_id[0][0], quantity = quantity, seller_id = seller_id, product_description = product_description, price = price)
        return True
    
    @staticmethod
    def edit_product(product_id, product_name, image_url, price, product_description, category_name, quantity):
        row = app.db.execute("""
UPDATE Products SET image_url = :image_url, product_name = :product_name, category_name = :category_name
WHERE product_id = :product_id
RETURNING product_id
""",
        product_id = product_id, image_url = image_url, product_name = product_name, category_name = category_name)
        seller_id = current_user.id
        col = app.db.execute("""
UPDATE Inventory SET quantity = :quantity, product_description = :product_description, price = :price
WHERE product_id = :product_id AND seller_id = :seller_id
RETURNING product_id
""",
        product_id = product_id, quantity = quantity, product_description = product_description, price = price, seller_id = seller_id)

        return True
