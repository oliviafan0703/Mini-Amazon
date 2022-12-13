import random
from werkzeug.security import generate_password_hash
import csv
from faker import Faker

num_users = 110
num_products = 200
num_orders = 250
num_reviews = 100
num_inventorys = 150

num_sellers = 30
num_cartItems = 8

Faker.seed(0)
fake = Faker()

CATEGORIES = [
  "Books",
  "Movies",
  "Music",
  "Games",
  "Electronics",
  "Computers",
  "Home",
  "Garden",
  "Tools",
  "Grocery",
  "Health",
  "Beauty",
  "Toys",
  "Kids",
  "Baby",
  "Clothing",
  "Shoes",
  "Jewelery",
  "Sports",
  "Outdoors",
  "Automotive",
  "Industrial"
]
num_categories = len(CATEGORIES)
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



def gen_products(num_products):
    available_pids = []
    with open('Products.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Products...', end=' ', flush=True)
        for product_id in range(num_products):
            if product_id % 10 == 0:
                print(f'{product_id}', end=' ', flush=True)
            product_name = fake.sentence(nb_words=5)[:-1]
            image_url = fake.image_url()
            product_description = fake.sentence(nb_words=20)[:-1]
            price = fake.random_int(min = 100, max=99000)/100
            quantity = fake.random_int(min=0, max=50)
            category_name = random.choice(CATEGORIES)
            writer.writerow([product_id, image_url, product_name, product_description, price, quantity, category_name])
        print(f'{num_products} generated; {len(available_pids)} available')
    return available_pids



def gen_categories(num_categories):
    with open('Categories.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Categories...', end=' ', flush=True)
        for id in range(num_categories):
            if id % 5 == 0:
                print(f'{id}', end=' ', flush=True)
            category_name = CATEGORIES[id]
            writer.writerow([category_name])
        print(f'{num_categories} generated')
    return
generated_seller_ids = []
def gen_sellers(num_sellers):
    with open('Sellers.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Sellers...', end=' ', flush=True)
        seen = set()
        for id in range(num_sellers):
            if id % 5 == 0:
                print(f'{id}', end=' ', flush=True)
            
            generated_id = fake.random_int(min=0, max=num_users-1)
            
            while generated_id in seen:
                generated_id = fake.random_int(min=0, max=num_users-1)

            seen.add(generated_id) 

            generated_seller_ids.append(generated_id)
            #yihougaiyixia 
            writer.writerow([generated_id])
        print(f'{num_sellers} generated')
    return

def gen_inventorys(num_inventorys):
    with open('Inventorys.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Inventorys...', end=' ', flush=True)
        for id in range(num_inventorys):
            if id % 10 == 0:
                print(f'{id}', end=' ', flush=True)
            seller_id = random.choice(generated_seller_ids)
            product_id = fake.random_int(min=0, max=num_products-1)
            quantity = fake.random_int(min=1, max=50)
            writer.writerow([product_id, quantity, seller_id])
        print(f'{num_inventorys} generated')
    return

def gen_carts(num_cartItems):
    with open('CartItems.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('CartItems...', end=' ', flush=True)
        for id in range(num_cartItems):
            if id % 5 == 0:
                print(f'{id}', end=' ', flush=True)
            quantity = fake.random_int(min=0, max=50)
            product_ID = fake.random_int(min=0, max=num_products-1)
            
            #seller id generating code here
            seller_id = random.choice(generated_seller_ids)
            # 
             
            u_id = fake.random_int(min=0, max=num_users-1)

            writer.writerow([quantity, product_ID, seller_id, u_id])
        print(f'{num_cartItems} generated')
    return

def gen_reviews(num_reviews):
    with open('Reviews.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Reviews...', end=' ', flush=True)
        for id in range(num_reviews):
            if id % 10 == 0:
                print(f'{id}', end=' ', flush=True)
            user_id = fake.random_int(min=0, max=num_users-1)
            product_id = fake.random_int(min=0, max=num_products-1)
            seller_id = random.choice(generated_seller_ids)
            title = fake.sentence(nb_words=5)[:-1]

            content = fake.sentence(nb_words=20)[:-1]
            rating = fake.random_int(min=0, max=5)
            time_post= fake.date_time()
            writer.writerow([user_id, product_id, seller_id, rating, title, content, time_post])
        print(f'{num_reviews} generated')
    return

def gen_order_details(num_orders):
    with open('Order_Details.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Orders...', end=' ', flush=True)


        for order_id in range(num_orders):
            for i in range(10):
                if order_id % 10 == 0:
                    print(f'{order_id}', end=' ', flush=True)
                product_id = fake.random_int(min=0, max=num_products-1)
                quantity = fake.random_int(min=0, max=50)
                order_timestamp= fake.date_time()
                fulfill_status = fake.random_element(elements=('true', 'false'))
                seller_id = random.choice(generated_seller_ids)
                writer.writerow([order_id, quantity, fulfill_status, order_timestamp, product_id, seller_id])
        print(f'{num_orders} generated')
    return

def gen_orders(num_orders):
    with open('Order.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Orders...', end=' ', flush=True)
        for order_id in range(num_orders):
            if order_id % 10 == 0:
                print(f'{order_id}', end=' ', flush=True)
            user_id = fake.random_int(min=0, max=num_users-1)
            writer.writerow([order_id, user_id])
        print(f'{num_orders} generated')
    return
# gen_users(num_users)

#gen_orders(num_orders)
# gen_reviews(num_reviews)
# gen_orders(num_orders)
# # print(gen_random_user_id(10))

gen_sellers(num_sellers)
gen_inventorys(num_inventorys)
gen_carts(num_cartItems)
gen_order_details(num_orders)
gen_orders(num_orders)
gen_reviews(num_reviews)
# gen_categories(num_categories)

# gen_products(num_products)