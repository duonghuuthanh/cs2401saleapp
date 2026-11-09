from eapp.models import Category, Product, User, Receipt, ReceiptDetails
from eapp import app, db
import hashlib
import cloudinary.uploader
from flask_login import current_user
from sqlalchemy import func

def load_categories():
    return Category.query.all()


def load_products(kw=None, cate_id=None, page=1):
    query = Product.query

    if kw:
        query = query.filter(Product.name.contains(kw))

    if cate_id:
        query = query.filter(Product.category_id==int(cate_id))

    page_size = app.config['PAGE_SIZE']
    start = (page - 1) * page_size

    query = query.slice(start, start + page_size)

    return query.all()

def count_products():
    return Product.query.count()

def authenticate(username, password):
    password = hashlib.md5(password.strip().encode('utf-8')).hexdigest()

    return User.query.filter(User.username.__eq__(username.strip()), User.password.__eq__(password)).first()

def get_user_by_id(user_id):
    return User.query.get(user_id)

def create_user(name, username, password, avatar=None):
    password = hashlib.md5(password.strip().encode('utf-8')).hexdigest()
    u = User(name=name.strip(), username=username.strip(), password=password, avatar=avatar)

    if avatar:
        res = cloudinary.uploader.upload(avatar)
        print(res)
        u.avatar = res.get('secure_url')

    db.session.add(u)
    db.session.commit()


def add_receipt(cart):
    if cart:
        r = Receipt(user=current_user)
        db.session.add(r)

        for c in cart.values():
            d = ReceiptDetails(quantity=c['quantity'], price=c['price'], receipt=r, product_id=c['id'])
            db.session.add(d)

        db.session.commit()


def count_products_by_cate():
    # [(1, 'Mobile', 6), (2, 'Tablet', 3), (3, 'Laptop', 0)]
    return (db.session.query(Category.id, Category.name, func.count(Product.id))
            .join(Product, Product.category_id==Category.id, isouter=True).group_by(Category.id).all())


if __name__ == '__main__':
    with app.app_context():
        print(count_products_by_cate())