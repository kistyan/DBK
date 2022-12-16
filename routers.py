from config import app
from flask import request, render_template, jsonify, url_for, make_response
import services, models


@app.route('/')
def index():
    role = services.get_role(request.cookies.get('loginpass'))
    return render_template('index.html', role=role)


@app.route('/backup.json')
def backup():
    if services.get_role(request.cookies.get('loginpass')) == 'admin':
        return services.backup()
    return 'Access denied'


@app.route('/Books', methods=['GET'])
def get_books():
    role = services.get_role(request.cookies.get('loginpass'))
    return render_template('books.html', books=services.get_books(), role=role)


@app.route('/BooksJSON', methods=['GET'])
def get_books_json():
    return str(services.get_books())


@app.route('/BooksCSV', methods=['GET'])
def get_books_csv():
    books = services.get_books()
    return services.get_csv(books)


@app.route('/Users', methods=['GET'])
def get_users():
    loginpass = request.cookies.get('loginpass')
    role = services.get_role(loginpass)
    user_id = services.get_uid(loginpass)
    return render_template('users.html', users=services.get_users(), role=role, user_id=user_id)


@app.route('/Profile', methods=['GET'])
def get_profile():
    loginpass = request.cookies.get('loginpass')
    user_data = services.get_user_data(services.get_uid(loginpass))
    return render_template(
        'profile.html',
        role=services.get_role(loginpass),
        name=user_data[0][0]['name'],
        balance=user_data[0][0]['balance'],
        history=user_data[1],
        favorite_books=user_data[2],
        purchased_books=user_data[3],
        reviews=user_data[4],
        promo_codes=user_data[5]
    )


@app.route('/UsersJSON', methods=['GET'])
def get_users_json():
    return str(services.get_users())


@app.route('/UsersCSV', methods=['GET'])
def get_users_csv():
    users = services.get_users()
    return services.get_csv(users)


@app.route('/Users/get_user_data', methods=['POST'])
def get_user_data():
    return services.get_user_data(request.form.to_dict()['user_id'])


@app.route('/Authors', methods=['GET'])
def get_authors():
    role = services.get_role(request.cookies.get('loginpass'))
    return render_template('authors.html', authors=services.get_authors(), role=role)


@app.route('/AuthorsJSON', methods=['GET'])
def get_authors_json():
    return str(services.get_authors())


@app.route('/AuthorsCSV', methods=['GET'])
def get_authors_csv():
    authors = services.get_authors()
    return services.get_csv(authors)


@app.route('/Publishers', methods=['GET'])
def get_publishers():
    role = services.get_role(request.cookies.get('loginpass'))
    return render_template('publishers.html', publishers=services.get_publishers(), role=role)


@app.route('/PublishersJSON', methods=['GET'])
def get_publishers_json():
    return str(services.get_publishers())


@app.route('/PublishersCSV', methods=['GET'])
def get_publishers_csv():
    publishers = services.get_publishers()
    return services.get_csv(publishers)


@app.route('/PromoCodes', methods=['GET'])
def get_promo_codes():
    role = services.get_role(request.cookies.get('loginpass'))
    return render_template('promo_codes.html', promo_codes=services.get_promo_codes(), role=role)


@app.route('/PromoCodesJSON', methods=['GET'])
def get_promo_codes_json():
    return str(services.get_promo_codes())


@app.route('/PromoCodesCSV', methods=['GET'])
def get_promo_codes_csv():
    promo_codes = services.get_promo_codes()
    return services.get_csv(promo_codes)


@app.route('/Reviews', methods=['GET'])
def get_reviews():
    loginpass = request.cookies.get('loginpass')
    role = services.get_role(loginpass)
    user_id = services.get_uid(loginpass)
    return render_template('reviews.html', reviews=services.get_reviews(), role=role, user_id=user_id)


@app.route('/ReviewsJSON', methods=['GET'])
def get_reviews_json():
    return str(services.get_reviews())


@app.route('/ReviewsCSV', methods=['GET'])
def get_reviews_csv():
    reviews = services.get_reviews()
    return services.get_csv(reviews)


@app.route('/Reviews/get_book_reviews', methods=['POST'])
def get_book_reviews():
    return services.get_book_reviews(request.form)


@app.route('/Books/add_book', methods=['POST'])
def add_book():
    book = request.form
    return services.add_book(book)


@app.route('/Users/add_user', methods=['POST'])
def add_user():
    user = request.form
    return services.add_user(user)


@app.route('/Authors/add_author', methods=['POST'])
def add_author():
    author = request.form
    return services.add_author(author)


@app.route('/Publishers/add_publisher', methods=['POST'])
def add_publisher():
    publisher = request.form
    return services.add_publisher(publisher)


@app.route('/PromoCodes/add_promo_code', methods=['POST'])
def add_promo_code():
    promo_code = request.form
    return services.add_promo_code(promo_code)


@app.route('/Reviews/add_review', methods=['POST'])
def add_review():
    review = request.form
    return services.add_review(review)


@app.route('/Books/del_book', methods=['POST'])
def del_book():
    book = request.form
    return {'id': services.del_book(book)}


@app.route('/Users/del_user', methods=['POST'])
def del_user():
    user = request.form
    return {'id': services.del_user(user)}


@app.route('/Authors/del_author', methods=['POST'])
def del_author():
    author = request.form
    return {'id': services.del_author(author)}


@app.route('/Publishers/del_publisher', methods=['POST'])
def del_publisher():
    publisher = request.form
    return {'id': services.del_publisher(publisher)}


@app.route('/PromoCodes/del_promo_code', methods=['POST'])
def del_promo_code():
    promo_code = request.form
    return {'id': services.del_promo_code(promo_code)}


@app.route('/Reviews/del_review', methods=['POST'])
def del_review():
    review = request.form
    return {'id': services.del_review(review)}


@app.route('/auth', methods=['POST'])
def auth():
    loginpass = request.form['login'] + request.form['pass']
    resp = jsonify(role=services.get_role(loginpass))
    resp.set_cookie('loginpass', loginpass)
    return resp
