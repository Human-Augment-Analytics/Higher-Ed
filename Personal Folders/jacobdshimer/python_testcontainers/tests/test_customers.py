from faker import Faker

from customers.customers import Customer, create_customer, get_all_customers, get_by_email


def test_get_by_email(faker: Faker):
    email = faker.email()
    name = faker.name()
    cust = Customer(email=email, name=name)
    create_customer(cust)

    found_cust = get_by_email(email)
    assert found_cust is not None
    assert found_cust.email == email
    assert found_cust.name == name


def test_get_all(faker: Faker):
    create_customer(Customer(email=faker.email(), name=faker.name()))
    create_customer(Customer(email=faker.email(), name=faker.name()))

    all_cust = get_all_customers()
    assert len(all_cust) == 2
