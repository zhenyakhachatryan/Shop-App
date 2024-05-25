from flask import Blueprint,request,url_for,session,redirect,render_template
from flask_mail import Message
from itsdangerous import SignatureExpired
from werkzeug.security import generate_password_hash
import random

email_bp=Blueprint('email',__name__)

    

@email_bp.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    session.pop('api_error', None)
    from models import User, ADMIN
    from app import mail
    if request.method == 'POST':
        email = request.form.get('email')
        if email:
            user = User.query.filter_by(email=email).first()
            admin = ADMIN.query.filter_by(email=email).first()
            account = user if user else admin
            if account:
                token = account.get_reset_token()
                reset_url = url_for('email.reset_with_token', token=token, _external=True)
                msg = Message('Password Reset Request', recipients=[email])
                msg.body = f'To reset your password, please click the following link: {reset_url}'
                mail.send(msg)
                session['api_error'] = {'message': 'An email with instructions to reset your password has been sent.'}
                return redirect(url_for('auth.user_login') if user else url_for('auth.admin_login'))
            else:
                session['api_error'] = {'message': 'Email not found in database. Please enter a valid email address.'}
        else:
            session['api_error'] = {'message': 'Please provide an email address.'}
    return render_template('reset_password.html')

@email_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_with_token(token):
    session.pop('api_error', None)
    from models import User
    from app import db

    try:
        account = User.verify_reset_token(token)
        if account is None:
            session['api_error'] = {'message': 'Invalid or expired token.'}
            return redirect(url_for('email.reset_password'))

        elif request.method == 'POST':
            new_password = request.form.get('new_password')
            confirm_password = request.form.get('confirm_password')
            if  len(new_password)<8 or (not any(i.isupper() for i in new_password) or not any(i.isdigit() for i in new_password)):
                session['api_error'] = {'error': 'Your password should have at least 8 characters and should contain at least 1 number and 1 capital letter.'}
            elif new_password and new_password == confirm_password:
                account.password = generate_password_hash(new_password)
                db.session.commit()
                session['api_error'] = {'message': 'Your password has been updated successfully.'}
                return redirect(url_for('auth.user_login') if isinstance(account, User) else url_for('auth.admin_login'))
            else:
                session['api_error'] = {'message': 'Passwords do not match. Please try again.'}
        return render_template('reset_with_token.html', token=token)
    except SignatureExpired:
        session['api_error'] ={'message':'The password reset link has expired. Please try again.'}
        return redirect(url_for('reset_password'))
    

def generate_verification_code():
    return ''.join([str(random.randint(0, 9)) for i in range(6)]) 

@email_bp.route('/send_verification_email', methods=['GET','POST'])
def send_verification_email():
    session.pop('api_error', None)
    from app import mail
    if request.method == 'POST':
        email = request.form.get('email')
        verification_code = generate_verification_code()
        session['verification_code'] = verification_code  
        session['email'] = email 

        msg = Message('Verification Code', recipients=[email])
        msg.body = f'Your verification code is: {verification_code}'
        mail.send(msg)
        session['api_error'] = {'message': 'Verification code sent successfully!'}
        return redirect(url_for('email.verify_email'))
    return render_template('user_email.html')
  

@email_bp.route('/verify_email', methods=['GET', 'POST'])
def verify_email():
    session.pop('api_error', None)
    if request.method == 'POST':
        user_verification_code = request.form.get('verification_code')
        if user_verification_code == session.get('verification_code'):
            session.pop('verification_code', None)
            session['api_error'] = {'message': 'Email verified successfully!'}
            return redirect(url_for('auth.user_register'))
        else:
            session['api_error'] = {'message': 'Invalid verification code. Please try again.'}

    return render_template('verify_email.html')



@email_bp.route('/send_admin_verification_email', methods=['GET','POST'])
def send_admin_verification_email():
    session.pop('api_error', None)
    from app import mail
    if request.method == 'POST':
        email = request.form.get('email')
        verification_code = generate_verification_code()
        session['verification_code'] = verification_code  
        session['email'] = email 

        msg = Message('Verification Code', recipients=[email])
        msg.body = f'Your verification code is: {verification_code}'
        mail.send(msg)
        session['api_error'] = {'message': 'Verification code sent successfully!'}
        return redirect(url_for('email.verify_admin_email'))
    return render_template('admin_email.html')


@email_bp.route('/verify_admin_email', methods=['GET', 'POST'])
def verify_admin_email():
    session.pop('api_error', None)
    if request.method == 'POST':
        user_verification_code = request.form.get('verification_code')
        if user_verification_code == session.get('verification_code'):
            session.pop('verification_code', None)
            session['api_error'] = {'message': 'Email verification successful!'}
            return redirect(url_for('auth.admin_register'))
        else:
            session['api_error'] = {'message': 'Invalid verification code. Please try again.'}

    return render_template('verify_admin_email.html')

