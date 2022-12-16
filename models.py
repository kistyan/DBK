import peewee as pw
from config import BaseModel, db


class Author(BaseModel):
    id = pw.IntegerField(primary_key=True)
    name = pw.CharField(max_length=256)


class Publisher(BaseModel):
    id = pw.IntegerField(primary_key=True)
    name = pw.CharField(max_length=256)
    address = pw.CharField(max_length=256)
    phone = pw.CharField(max_length=25)


class Book(BaseModel):
    id = pw.IntegerField(primary_key=True)
    author_id = pw.IntegerField()
    publisher_id = pw.IntegerField()
    name = pw.CharField(max_length=256)
    genre = pw.CharField(max_length=256)
    price = pw.FloatField()


class User(BaseModel):
    id = pw.IntegerField(primary_key=True)
    name = pw.CharField(max_length=256)
    balance = pw.FloatField()
    loginpass = pw.CharField(max_length=256)
    role = pw.CharField(max_length=256)


class FavoriteBook(BaseModel):
    id = pw.IntegerField(primary_key=True)
    book_id = pw.IntegerField()
    user_id = pw.IntegerField()


class Receipt(BaseModel):
    id = pw.IntegerField(primary_key=True)
    user_id = pw.IntegerField()
    date = pw.DateTimeField()
    total = pw.FloatField()


class PurchasedBook(BaseModel):
    id = pw.IntegerField(primary_key=True)
    book_id = pw.IntegerField()
    receipt_id = pw.IntegerField()


class Review(BaseModel):
    id = pw.IntegerField(primary_key=True)
    book_id = pw.IntegerField()
    user_id = pw.IntegerField()
    grade = pw.IntegerField()
    text = pw.CharField(max_length=256)


class View(BaseModel):
    id = pw.IntegerField(primary_key=True)
    book_id = pw.IntegerField()
    user_id = pw.IntegerField()
    date = pw.DateTimeField()


class PromoCode(BaseModel):
    id = pw.IntegerField(primary_key=True)
    book_id = pw.IntegerField()
    code = pw.CharField(max_length=256)
    discount = pw.FloatField()
    valid_until = pw.DateTimeField()


class ReceivedPromoCode(BaseModel):
    id = pw.IntegerField(primary_key=True)
    promo_code_id = pw.IntegerField()
    user_id = pw.IntegerField()


with db:
    db.create_tables([
        Author, Publisher, Book, User, FavoriteBook, Receipt,
        PurchasedBook, Review, View, PromoCode, ReceivedPromoCode
    ])
