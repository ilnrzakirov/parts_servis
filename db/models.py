import sqlalchemy
from passlib.hash import bcrypt
from sqlalchemy import (
    VARCHAR,
    Column,
    ForeignKey,
    Integer,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

BaseModel = declarative_base()


class User(BaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(VARCHAR(255), nullable=False, unique=True)
    password = Column(VARCHAR(500), nullable=False)
    email = Column(VARCHAR(300), nullable=False, unique=True)

    def __init__(self, username, password, email):
        self.username = username
        self.password = bcrypt.encrypt(password)
        self.email = email

    def password_is_valid(self, password):
        return bcrypt.verify(password, self.password)

    def __str__(self):
        return self.username


class Company(BaseModel):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(255), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class Category(BaseModel):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(255), unique=True)
    product = relationship("products", secondary="association", backref="categories")

    def __str__(self):
        return self.name

    def __init__(self, name):
        self.name = name


association = sqlalchemy.Table(
    "association", BaseModel.metadata,
    Column("product_id", Integer, ForeignKey("products.id")),
    Column("category_id", Integer, ForeignKey("categories.id")),
)


class Product(BaseModel):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    category = relationship("categories", secondary="association", backref="products")
    balance = Column(Integer, nullable=False)
    company = Column(Integer, ForeignKey("companies.id"))
    name = Column(VARCHAR(255), nullable=False)
    price = Column(Integer, nullable=False)

    def __str__(self):
        return self.name

    def __init__(self, name, balance, company_id, price):
        self.name = name
        self.balance = balance
        self.company = company_id
        self.price = price