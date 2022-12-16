import datetime
import os
from flask import current_app, send_file
import models
from peewee import fn
from playhouse.shortcuts import model_to_dict

from config import app


def execute_get_all(model):
    query = model.select()
    return [model_to_dict(model) for model in query]


def execute_get_one(pk, model):
    query = model.select().where(model.id == int(pk))
    return [model_to_dict(model) for model in query]


def get_books():
    query = models.Book.select().order_by(models.Book.name)
    return [model_to_dict(model) for model in query]


def get_users():
    query = models.User.select(models.User.id, models.User.name, models.User.balance, models.User.role)\
        .order_by(models.User.name)
    return [model_to_dict(model) for model in query]


def get_authors():
    query = models.Author.select().order_by(models.Author.name)
    return [model_to_dict(model) for model in query]


def get_publishers():
    query = models.Publisher.select().order_by(models.Publisher.name)
    return [model_to_dict(model) for model in query]


def get_promo_codes():
    query = models.PromoCode.select().order_by(models.PromoCode.valid_until)
    return [model_to_dict(model) for model in query]


def get_reviews():
    query = models.Review.select().order_by(models.Review.grade)
    return [model_to_dict(model) for model in query]


def get_book_reviews(json):
    book_id = json.to_dict()['book_id']
    if book_id == '':
        return get_reviews()
    else:
        query = models.Review.select().where(models.Review.book_id == book_id)
    return [model_to_dict(model) for model in query]


def get_user_data(json):
    user_id = json.to_dict()['user_id']
    data = [
        models.User.select().where(models.User.id == user_id),
        reversed(models.View.select().where(models.View.user_id == user_id).order_by(models.View.date)),
        [models.Book.select().where(models.Book.id == favorite_model.book_id)[0]
         for favorite_model in
         models.FavoriteBook.select().where(models.FavoriteBook.user_id == user_id)],
        models.Receipt.select(
            models.Book.id,
            models.Book.author_id,
            models.Book.publisher_id,
            models.Book.name,
            models.Book.genre,
            models.Book.price,
            models.Receipt.date
        ).where(models.Receipt.user_id == user_id).join(
            models.PurchasedBook,
            on=(models.Receipt.id == models.PurchasedBook.receipt_id)
        ).join(
            models.Book,
            on=(models.PurchasedBook.book_id == models.Book.id)
        ).group_by(models.Book.id),
        models.Review.select().where(models.Review.user_id == user_id),
        [models.PromoCode.select().where(models.PromoCode.id == received_model.promo_code_id)[0]
         for received_model in
         models.ReceivedPromoCode.select().where(models.ReceivedPromoCode.user_id == user_id)]
    ]
    data_3 = []
    for row in data[3].namedtuples():
        data_3.append({
            'id': row.id,
            'author_id': row.author_id,
            'publisher_id': row.publisher_id,
            'name': row.name,
            'genre': row.genre,
            'price': row.price,
            'date': row.date
        })
    data[3] = data_3
    return [[(row if type(row) is dict else model_to_dict(row)) for row in table] for table in data]


def add_row(row, model):
    model.create(**row)


def get_free_id(model):
    free_id = model.select().count()
    for i in range(free_id):
        if not model.select().where(model.id == i):
            free_id = i
            break
    return free_id


def add_record(model, json):
    if not (type(json) is dict):
        json = json.to_dict()
    json['id'] = get_free_id(model)
    return model_to_dict(model.create(**json))


def add_book(json):
    return add_record(models.Book, json)


def add_user(json):
    if not (type(json) is dict):
        json = json.to_dict()
    json['id'] = get_free_id(models.User)
    json['balance'] = 0
    return model_to_dict(models.User.create(**json))


def add_author(json):
    return add_record(models.Author, json)


def add_publisher(json):
    return add_record(models.Publisher, json)


def add_promo_code(json):
    return add_record(models.PromoCode, json)


def add_review(json):
    return add_record(models.Review, json)


def del_record(model, json):
    del_id = json.to_dict()["id"]
    model.delete().where(model.id == del_id).execute()
    return del_id


def del_book(json):
    return del_record(models.Book, json)


def del_user(json):
    return del_record(models.User, json)


def del_author(json):
    return del_record(models.Author, json)


def del_publisher(json):
    return del_record(models.Publisher, json)


def del_promo_code(json):
    return del_record(models.PromoCode, json)


def del_review(json):
    return del_record(models.Review, json)


def get_role(loginpass):
    try:
        role = model_to_dict(models.User.select().where(models.User.loginpass == loginpass)[0])['role']
    except:
        role = ''
    return role


def get_uid(loginpass):
    try:
        return model_to_dict(models.User.select().where(models.User.loginpass == loginpass)[0])['id']
    except:
        return -1


def get_csv(json):
    csv = ''
    if len(json):
        keys = list(json[0].keys())
        for key_i in range(len(keys)):
            csv += (',' if key_i else '') + '"' + keys[key_i] + '"'
        csv += '\n'
        for row_i in range(len(json)):
            values = list(json[row_i].values())
            for value_i in range(len(values)):
                csv += (',' if value_i else '') + '"' + str(values[value_i]) + '"'
            csv += '\n'
    return csv


def backup():
    tables = {
        'author_table': models.Author,
        'publisher_table': models.Publisher,
        'book_table': models.Book,
        'user_table': models.User,
        'favorite_book_table': models.FavoriteBook,
        'receipt_table': models.Receipt,
        'purchased_book_table': models.PurchasedBook,
        'review_table': models.Review,
        'view_table': models.View,
        'promo_code_table': models.PromoCode,
        'received_promo_code_table': models.ReceivedPromoCode
    }
    json = {}
    for table in tables:
        json[table] = [model_to_dict(row) for row in tables[table].select()]
    with open('backup.json', 'w') as outfile:
        outfile.write(str(json))
    return send_file('backup.json', as_attachment=True)
