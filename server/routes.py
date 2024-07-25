from flask import Blueprint, request, jsonify, send_from_directory
from server.models import db, User, Animal, Order, Cart, OrderItem, CartItem, Token
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from server.config import Config
import os

api_bp = Blueprint('api', __name__)

@api_bp.route('/')
def index():
    return "Welcome to Farmart API!"

@api_bp.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(api_bp.root_path, 'static'), 'favicon.ico')

@api_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(username=data['username'], password=hashed_password, user_type=data['user_type'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'})

@api_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password, data['password']):
        token = jwt.encode({'id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)}, Config.JWT_SECRET_KEY)
        new_token = Token(user_id=user.id, token=token)
        db.session.add(new_token)
        db.session.commit()
        return jsonify({'token': token})
    return jsonify({'message': 'Invalid credentials'})

@api_bp.route('/animals', methods=['POST'])
def add_animal():
    data = request.get_json()
    new_animal = Animal(name=data['name'], price=data['price'], image_url=data['image_url'], user_id=data['user_id'])
    db.session.add(new_animal)
    db.session.commit()
    return jsonify({'message': 'Animal added successfully'})

@api_bp.route('/cart', methods=['GET', 'POST'])
def handle_cart():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Token is missing!'}), 401
    try:
        data = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
        user = User.query.get(data['id'])
    except:
        return jsonify({'message': 'Token is invalid!'}), 401

    if request.method == 'POST':
        animal_id = request.get_json()['animal_id']
        cart_item = CartItem(cart_id=user.cart.id, animal_id=animal_id)
        db.session.add(cart_item)
        db.session.commit()
        return jsonify({'message': 'Item added to cart'})
    else:
        items = [{'animal_id': item.animal_id, 'animal_name': item.animal.name, 'price': item.animal.price} for item in user.cart.items]
        return jsonify(items)

@api_bp.route('/checkout', methods=['POST'])
def checkout():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Token is missing!'}), 401
    try:
        data = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
        user = User.query.get(data['id'])
    except:
        return jsonify({'message': 'Token is invalid!'}), 401

    order = Order(user_id=user.id)
    db.session.add(order)
    db.session.commit()
    for item in user.cart.items:
        order_item = OrderItem(order_id=order.id, animal_id=item.animal_id)
        db.session.add(order_item)
    db.session.commit()

    user.cart.items = []
    db.session.commit()

    return jsonify({'message': 'Order placed successfully'})
