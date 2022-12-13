
from faker import Faker
import faker_commerce

fake = Faker()
fake.add_provider(faker_commerce.Provider)
def gen_products(num_products):
    product_name = fake.sentence(nb_words=5)[:-1]
    url = fake.image_url()
    productName = fake.ecommerce_name()
    price = fake.ecommerce_price(False)
    print(url)
    print(productName)
    print(price)
    # # *image_url = fake.internet.avatar()
    #         product_description = fake.sentence(nb_words=20)[:-1]
    #         # *price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'

    return 0

gen_products(5)