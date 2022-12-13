import random
from werkzeug.security import generate_password_hash
import csv
from faker import Faker
from re import sub
from decimal import Decimal
num_users = 110
num_products = 200
num_orders = 250
num_reviews = 100
num_inventorys = 150

num_sellers = 30
num_cartItems = 8


import pandas as pd
fields = ['Product Name', "Category" ,'Selling Price','About Product','Image', 'Unique_Category']
df = pd.read_csv('processed_data.csv', skipinitialspace=True, usecols=fields)
# See the keys
print(df.keys())
# See content in 'star_name'
print (type(df['Product Name']))
print(df.head(5))



Faker.seed(0)
fake = Faker()

def get_csv_writer(f):
    return csv.writer(f, dialect='unix')

def gen_users(num_users):
    with open('Users.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Users...', end=' ', flush=True)
        for id in range(num_users):
            if id % 10 == 0:
                print(f'{id}', end=' ', flush=True)
            profile = fake.profile()
            email = profile['mail']
            plain_password = f'pass{id}'
            password = generate_password_hash(plain_password)
            name_components = profile['name'].split(' ')
            firstname = name_components[0]
            lastname = name_components[-1]
            mailing_address = fake.address()
            balance = f'{str(fake.random_int(max=100000))}.{fake.random_int(max=99):02}'
            writer.writerow([id, email, password, firstname, lastname, mailing_address, balance])
        print(f'{num_users} generated')
    return

#generate products
# name,category,price, description, url
my_products = {}
def gen_products():
    with open('Products.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Users...', end=' ', flush=True)
        # for id in range(num_users):
        for index, info in df.iterrows():
            my_products[index] = info
            category = info["Unique_Category"]
            description = info["About Product"]
            if pd.isnull(description):
                info["About Product"] = "This product is a great buy!"
            name= info ["Product Name"]
            image_url = info['Image'].split("|")[0]
            owner_id = 0
            # print(image_url)
            writer.writerow([index,image_url, name, category, owner_id])
        print(f'{index} generated')
    return


categories = []
for index, info in df.iterrows():
    category = info["Unique_Category"]
    if category not in categories:
        categories.append(category)

print(len(categories))
# gen_users(1000)
gen_products()

def gen_categories():
    with open('Categories.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Categories...', end=' ', flush=True)
        for category in categories:
            writer.writerow([category])
        print("generated categories")
    return
gen_categories()

#first 50 users are sellers

def gen_sellers():
    with open('Sellers.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Sellers...', end=' ', flush=True)
        for id in range(250):
            if id % 5 == 0:
                print(f'{id}', end=' ', flush=True)
            
            
            

            #yihougaiyixia 
            writer.writerow([id])
        print(f'{250} sellers generated')
    return

gen_sellers()

inventory = []
def gen_inventorys():
    with open('Inventorys.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Inventorys...', end=' ', flush=True)

        #for each product, make it have two sellers 
        for index, info in my_products.items():
            #have 2 sellers 
            for i in range(random.randint(4,5)):
                seller_id = random.randint(0,249)
                product_id = index
                quantity = fake.random_int(min=5, max=50)
                product_description = info['About Product'][0:254]

                raw_price= (info["Selling Price"])
                if " " in raw_price:
                    raw_price = fake.random_int(min = 100, max=99000)/100
                else:
                    raw_price = Decimal(sub(r'[^\d.]', '', raw_price))
                
                raw_price += random.randint(1,100)
                quantity = fake.random_int(min=0, max=50)
                inventory.append([product_id, quantity, seller_id, product_description, raw_price])
                writer.writerow([product_id, quantity, seller_id, product_description, raw_price])
        print(f'{5} inven generated')
    return
gen_inventorys()

#users 50-109 purchased


def gen_orders():
    order_id = 0
    with open('Order.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Orders...', end=' ', flush=True)
       
        for user_id in range(50,999):
            for i in range(random.randint(4,10)):
                writer.writerow([order_id, user_id])
                order_id += 1
        print(f'{num_orders} generated')
    return

gen_orders()

pids = []
sids = []




def gen_order_details():
    with open('Order_Details.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Orders...', end=' ', flush=True)
        order_id = 6627
        for id in range(order_id):
            for i in range(random.randint(1,5)):
                if id % 10 == 0:
                    print(f'{id}', end=' ', flush=True)

                #seller:
                inven_idx = random.randint(0,len(inventory)-1)

                product_id = inventory[inven_idx][0]
                seller_id = inventory[inven_idx][2]
                
                quantity = random.randint(1,50)
                order_timestamp= fake.date_time()
                fulfill_timestamp= fake.date_time()
                fulfill_status = fake.random_element(elements=('true', 'false'))
                writer.writerow([id, quantity, fulfill_status, order_timestamp, fulfill_timestamp, product_id, seller_id])
        print(f'{num_orders} generated')
    return
gen_order_details()


colnames=['count','title','content'] 
df2 = pd.read_csv('test.csv', skipinitialspace=True, names = colnames)
# See the keys
print(df2.keys())
# See content in 'star_name'
# print(df2.head(5))




def gen_reviews_product():
    with open('ProductReviews.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('ProductReviews...', end=' ', flush=True)
        for id in range(3500):
            if id % 10 == 0:
                print(f'{id}', end=' ', flush=True)
            user_id = random.randint(50,999)
            product_id = random.randint(0,845)
            
            title = df2["title"][id%830]
            content = df2["content"][id%830][0:254]
            rating = fake.random_int(min=0, max=5)
            time_post= fake.date_time()
            writer.writerow([user_id, product_id, rating, title, content, time_post, 0])
        print(f'{num_reviews} generated')
    return

def gen_reviews_seller():
    with open('SellerReviews.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('ProductReviews...', end=' ', flush=True)
        for id in range(300):
            if id % 10 == 0:
                print(f'{id}', end=' ', flush=True)
            user_id = random.randint(50,999)
            seller_id = random.randint(0,49)
            title = df2["title"][id]
            content = df2["content"][id][0:254]
            rating = fake.random_int(min=0, max=5)
            time_post= fake.date_time()
            writer.writerow([user_id, seller_id, rating, title, content, time_post, 0])
        print(f'{num_reviews} generated')
    return

gen_reviews_product()

gen_reviews_seller()