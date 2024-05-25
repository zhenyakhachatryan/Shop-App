from datetime import datetime
import json
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

file_path = os.path.join(script_dir, 'product_data.json')

def export_product_data():
    from models import Product
    products = Product.query.all()

    
    product_data = []
    for product in products:
        product_data.append({
            'id': product.id,
            'category': product.category,
            'image': product.picture,
            'name': product.name,
            'quantity': product.quantity,
            'price': product.price,
            'description': product.description,
            'rate': product.rate,
            'insert_date': product.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })

    with open(file_path, 'w') as file:
        json.dump(product_data, file, indent=4)

def import_product_data():
    from models import db, Product
    script_dir = os.path.dirname(os.path.abspath(__file__))

    file_path = os.path.join(script_dir, 'product_data.json')
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print("File not found!")
        return
    except json.JSONDecodeError:
        print("Invalid JSON format!")
        return

    
    products_to_add = []
    for item in data:
        created_at = datetime.strptime(item.get('insert_date'), '%Y-%m-%d %H:%M:%S')
        product = Product(
            id=item.get('id'),
            category=item.get('category'),
            picture=item.get('image'),
            name=item.get('name'),
            quantity=item.get('quantity'),
            price=item.get('price'),
            description=item.get('description'),
            rate=item.get('rate'),
            created_at=created_at
        )
        products_to_add.append(product)

    db.session.add_all(products_to_add)
    db.session.commit()

def export_user_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    file_path = os.path.join(script_dir, 'user_data.json')
    from models import User
    users = User.query.all()

    
    user_data = []
    for user in users:
        user_data.append({
            'id':user.id,
            'username':user.username,
            'password':user.password,
            'email':user.email
        })

    with open(file_path, 'w') as file:
        json.dump(user_data, file, indent=4)

def import_user_data():
    from models import db, User
    script_dir = os.path.dirname(os.path.abspath(__file__))

    file_path = os.path.join(script_dir, 'user_data.json')
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print("File not found!")
        return
    except json.JSONDecodeError:
        print("Invalid JSON format!")
        return

    
    
    user_to_add = []
    for user in data:
        
        product = User(
            id=user.get('id'),
            username=user.get('username'),
            password=user.get('password'),
            email=user.get('email')   
        )
        user_to_add.append(product)

    db.session.add_all(user_to_add)
    db.session.commit()