from flask import Blueprint,render_template,redirect,url_for,request,session
from flask_login import login_user,logout_user
from werkzeug.security import check_password_hash,generate_password_hash
import uuid


auth_bp=Blueprint('auth',__name__)

def generate_api_key():
    return str(uuid.uuid4())


@auth_bp.route('/admin_register',methods=['GET','POST'])
def admin_register():
    session.pop('api_error', None) 
    from models import db,ADMIN
    if request.method=='POST':
        username = request.form.get('username')
        password = request.form.get('password')
        

        if not all([username, password]):
             session['api_error'] = {'error': 'Invalid data provided'}
        else:
            email = session.get('email')  
            if not email:
                session['api_error'] = {'error': 'Email not found in session. Please verify your email first.'}
                return redirect(url_for('pages.home_page')) 
            else:
                user_email=ADMIN.query.filter_by(email=email).first()
                user_name=ADMIN.query.filter_by(username=username).first()
                if user_email:
                    session['api_error'] = {'error': 'Email is already taken. Please choose another one'}

                elif user_name:
                    session['api_error'] = {'error': 'Username is already taken. Please choose another one'}
                elif len(username)<3:
                    session['api_error'] = {'error': 'Your username should have at least 3 characters'}

                elif  len(password)<8 or (not any(i.isupper() for i in password) or not any(i.isdigit() for i in password)):
                    session['api_error'] = {'error': 'Your password should have at least 8 characters and should contain at least 1 number and 1 capital letter.'}    
                        
                else:
                        hashed_password=generate_password_hash(password)
                        new_user=ADMIN(username=username,password=hashed_password,email=email)
                        db.session.add(new_user)
                        db.session.commit()
                        session.pop('email', None)
                        return redirect(url_for('auth.admin_login'))
  
    return render_template('admin_register.html')

@auth_bp.route('/google/authorized')
def google_authorized():
    session.pop('api_error', None) 
    from models import db,User 
    from flask_dance.contrib.google import google
    if not google.authorized:
            return redirect(url_for("google.login"))
    elif google.authorized:
            resp = google.get("/oauth2/v2/userinfo")
            print("OAuth response status code:", resp.status_code)
            print("OAuth response data:", resp.json())
            if resp.ok:
                user_info = resp.json()
                email = user_info["email"]
                existing_user = User.query.filter_by(email=email).first()
                if existing_user:
                    login_user(existing_user)
                    session["user_id"] = existing_user.id
                    return redirect(url_for('pages.profile',user_id=existing_user.id))
                else:
                    new_user = User(username=email.split('@')[0],email=email)
                    db.session.add(new_user)
                    db.session.commit()
                    login_user(new_user)
                    session["user_id"] = new_user.id
                    return redirect(url_for('pages.profile',user_id=new_user.id))
    session['api_error'] = {'error': 'Registration failed'}
    return render_template('user_register.html')


@auth_bp.route('/user_register',methods=['GET','POST'])
def user_register():
    session.pop('api_error', None) 
    from models import db,User 
    if request.method=='POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not all([username, password]):
             session['api_error'] = {'error': 'Invalid data provided'}
        else:
            email = session.get('email')  
            if not email:
                session['api_error'] = {'error': 'Email not found in session. Please verify your email first.'}
                return redirect(url_for('pages.home_page')) 
            else:
                user_email=User.query.filter_by(email=email).first()
                user_name=User.query.filter_by(username=username).first()
                if user_email:
                    session['api_error'] = {'error': 'Email is already taken. Please choose another one'}

                elif user_name:
                    session['api_error'] = {'error': 'Username is already taken. Please choose another one'}
                elif len(username)<3:
                    session['api_error'] = {'error': 'Your username should have at least 3 characters'}

                elif  len(password)<8 or (not any(i.isupper() for i in password) or not any(i.isdigit() for i in password)):
                    session['api_error'] = {'error': 'Your password should have at least 8 characters and should contain at least 1 number and 1 capital letter.'}    
                else:
                        user_api=generate_api_key()
                        hashed_password=generate_password_hash(password)
                        new_user=User(username=username,password=hashed_password,email=email,user_api=user_api)
                        db.session.add(new_user)
                        db.session.commit()
                        session.pop('email', None)
                        return redirect(url_for('auth.user_login'))
    return render_template('user_register.html')



@auth_bp.route('/user_login',methods=['GET','POST'])
def user_login():
    session.pop('api_error', None) 
    from models import User
    if request.method=='POST':
        email = request.form.get('email')
        password = request.form.get('password')
            
        
        user=User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password,password):
                login_user(user)
                session['user_id']=user.id
                session.pop('api_error', None) 
                return redirect(url_for('pages.profile',user_id=user.id))
        elif user and not check_password_hash(user.password, password):
                session['api_error'] = {'error': 'Invalid email or password'}
                 
        else:
                session['api_error'] = {'error': 'User not found. You have to register first!'}
    return render_template('user_login.html')
        
@auth_bp.route('/admin_login',methods=['GET','POST'])
def admin_login():
    from models import ADMIN
    if request.method=='POST':
        email = request.form.get('email')
        password = request.form.get('password')
        admin=ADMIN.query.filter_by(email=email).first()
        if admin and check_password_hash(admin.password,password):
            login_user(admin)
            session['admin_id']=admin.id
            session.pop('api_error', None)
            return redirect(url_for('admin.index'))
        elif admin and not check_password_hash(admin.password, password):
            session['api_error'] = {'error': 'Invalid email or password'} 
            
        else:
            session['api_error'] = {'error': 'User not found. You have to register first!'}
            
             
    return render_template('admin_login.html')


@auth_bp.route('/admin_logout')
def admin_logout():
    logout_user() 
    session.pop('admin_id', None)
    return redirect(url_for('auth.admin_login')) 
    

@auth_bp.route('/user_logout/')
def user_logout():
    if 'google_token' in session:
        logout_user()
        session.pop('user_id', None)
        session.pop('google_token', None)
        return redirect(url_for('pages.home_page'))  
    else:
        logout_user()
        session.pop('user_id', None)
        return redirect(url_for('pages.home_page'))
    

