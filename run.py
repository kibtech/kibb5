from app import create_app, db
from app.models import User, Product, Order, OrderItem, Payment, Commission, Wallet, Withdrawal, Category, Brand, ProductImage, Cart, CartItem
import os

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Product': Product,
        'Order': Order,
        'OrderItem': OrderItem,
        'Payment': Payment,
        'Commission': Commission,
        'Wallet': Wallet,
        'Withdrawal': Withdrawal,
        'Category': Category,
        'Brand': Brand,
        'ProductImage': ProductImage,
        'Cart': Cart,
        'CartItem': CartItem
    }

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)