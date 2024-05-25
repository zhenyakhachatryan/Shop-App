from flask import Blueprint,render_template
from flask_login import login_required


page_bp=Blueprint('pages',__name__)

@page_bp.route('/')
def home_page():
        return render_template('index.html')

@page_bp.route('/profile',methods=['GET','POST'])
@login_required
def profile():
    return render_template('profile.html')

@page_bp.route('/all_products')
def all_products():
        return render_template('products.html')

@page_bp.route('/single_products')
def single_products():
        return render_template('single_product.html')

@page_bp.route('/about')
def about():
        return render_template('about.html')

@page_bp.route('/contact')
def contact():
        return render_template('contact.html')

@page_bp.route('/user_email')
def user_email():
       return render_template('user_email.html')

@page_bp.route('/admin_email')
def admin_email():
       return render_template('admin_email.html')