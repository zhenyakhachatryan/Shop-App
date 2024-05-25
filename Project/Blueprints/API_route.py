from flask import Blueprint,jsonify,session,send_file,request,abort
from functools import wraps
from flask_restful import Resource

api_bp=Blueprint('api',__name__)


@api_bp.route('/single_product')
def single_product(product_id):
    from models import Product
    singal_product=Product.query.get_or_404(product_id)
    product_data={
        'id':singal_product.id,
        'category':singal_product.category,
        'image':singal_product.picture,
        'name':singal_product.name,
        'quantity':singal_product.quantity,
        'price':singal_product.price,
        'description':singal_product.description,
        'rate':singal_product.rate,
        'insert_date':singal_product.created_at

    }

    return jsonify(product_data)



@api_bp.route('/user')
def user():
    from models import User
    user_id=session['user_id']
    user_data=[]
    user=User.query.filter_by(id=user_id).first()
    user_dict={
            'id':user.id,
            'username':user.username,
            'email':user.email,

    }
    user_data.append(user_dict)

    return jsonify(user_data)


@api_bp.route('/products')
def products():
    return send_file('product_data.json')
    



@api_bp.route('/man_products')
def man_products():
    from models import Product
    man_products=Product.query.filter_by(category='man').all()
    product_data=[]
    for product in man_products:
        product_dict={
            'id':product.id,
            'category':product.category,
            'image':product.picture,
            'name':product.name,
            'quantity':product.quantity,
            'price':product.price,
            'description':product.description,
            'rate':product.rate,
            'insert_date':product.created_at
        }
        product_data.append(product_dict)
    return jsonify(product_data)




@api_bp.route('/woman_products')
def woman_products():
    from models import Product
    woman_products=Product.query.filter_by(category='woman').all()
    product_data=[]
    for product in woman_products:
        product_dict={
            'id':product.id,
            'category':product.category,
            'image':product.picture,
            'name':product.name,
            'quantity':product.quantity,
            'price':product.price,
            'description':product.description,
            'rate':product.rate,
            'insert_date':product.created_at
        }
        product_data.append(product_dict)
    return jsonify(product_data)



@api_bp.route('/kid_products')
def kid_products():
    from models import Product
    kid_products=Product.query.filter_by(category='kid').all()
    product_data=[]
    for product in kid_products:
        product_dict={
            'id':product.id,
            'category':product.category,
            'image':product.picture,
            'name':product.name,
            'quantity':product.quantity,
            'price':product.price,
            'description':product.description,
            'rate':product.rate,
            'insert_date':product.created_at
        }
        product_data.append(product_dict)
    return jsonify(product_data)



@api_bp.route('/handle_errors', methods=['GET', 'POST'])
def handle_errors():
    error=session.pop('api_error', None)
    if error:
        return jsonify(error)
    return jsonify({'message':'No error found'})
        



def create_api_key(func):
    from models import User
    @wraps(func)
    def wrapper(*args,**kwargs):
        api_key=request.args.get('api_key')
        user=User.query.filter_by(user_api=api_key).first()
        if not user:
            abort(401, "Unauthorized:Invalid API key") 
        return func(*args,**kwargs)
    return wrapper      


class ProductResource(Resource):

    @create_api_key
    def get(self):
        from models import Product
        category = request.args.get('category')
        name = request.args.get('name')
        price = request.args.get('price')
        rate = request.args.get('rate')
        product_data=[]
        

        if category:
            products = Product.query.filter(Product.category.ilike(f'%{category}%')).all()
            
            for product in products:
                product_dict={
                    'id':product.id,
                    'category':product.category,
                    'image':product.picture,
                    'name':product.name,
                    'quantity':product.quantity,
                    'price':product.price,
                    'description':product.description,
                    'rate':product.rate,
                    'insert_date':product.created_at
                }
                product_data.append(product_dict)
        elif name:
            products = Product.query.filter(Product.name.ilike(f'%{name}%')).all()
            
            for product in products:
                product_dict={
                    'id':product.id,
                    'category':product.category,
                    'image':product.picture,
                    'name':product.name,
                    'quantity':product.quantity,
                    'price':product.price,
                    'description':product.description,
                    'rate':product.rate,
                    'insert_date':product.created_at
                }
                product_data.append(product_dict)

        elif price:
            products = Product.query.filter(Product.price.ilike(f'%{price}%')).all()
            
            for product in products:
                product_dict={
                    'id':product.id,
                    'category':product.category,
                    'image':product.picture,
                    'name':product.name,
                    'quantity':product.quantity,
                    'price':product.price,
                    'description':product.description,
                    'rate':product.rate,
                    'insert_date':product.created_at
                }
                product_data.append(product_dict)
        elif rate:
            products = Product.query.filter(Product.rate.ilike(f'%{rate}%')).all()
            
            for product in products:
                product_dict={
                    'id':product.id,
                    'category':product.category,
                    'image':product.picture,
                    'name':product.name,
                    'quantity':product.quantity,
                    'price':product.price,
                    'description':product.description,
                    'rate':product.rate,
                    'insert_date':product.created_at
                }
                product_data.append(product_dict)
        else:
            products=Product.query.all()
            for product in products:
                product_dict={
                    'id':product.id,
                    'category':product.category,
                    'image':product.picture,
                    'name':product.name,
                    'quantity':product.quantity,
                    'price':product.price,
                    'description':product.description,
                    'rate':product.rate,
                    'insert_date':product.created_at
                }
                product_data.append(product_dict)
        return jsonify(product_data) 
       
