from faker import Faker

from db.connection import Connection
from customers import customers

if __name__ == '__main__':
    faker = Faker()
    faker.seed_instance(0)
    conn = Connection.init()
    conn.init_db()

    for i in range(5):
        cust = customers.Customer(email=faker.email(), name=faker.name())
        customers.create_customer(cust)

    all_results = customers.get_all_customers()
    for i in all_results:
        print(i)

    print('---')

    single_result = customers.get_by_email(all_results[0].email)
    print(i)

    customers.delete_all_customers()
