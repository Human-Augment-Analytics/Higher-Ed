from pydantic import EmailStr
from sqlmodel import Field, SQLModel, select, delete

from db.connection import Connection


class Customer(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: EmailStr = Field(unique=True)
    name: str


def get_all_customers():
    with Connection.instance().get_session() as session:
        statement = select(Customer)
        return session.exec(statement).all()


def get_by_email(email: str):
    with Connection.instance().get_session() as session:
        statement = select(Customer).where(Customer.email == email)
        return session.exec(statement).first()


def create_customer(customer: Customer):
    with Connection.instance().get_session() as session:
        session.add(customer)
        session.commit()


def delete_all_customers():
    with Connection.instance().get_session() as session:
        session.exec(delete(Customer))
        session.commit()
