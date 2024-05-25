import os


base_dir=os.path.abspath(os.path.dirname(__file__))
db_path=os.path.join(base_dir,'Project.db')




SQLALCHEMY_DATABASE_URI = 'sqlite:///' + db_path
SECRET_KEY =  os.environ.get('SECRET_KEY')
MAIL_SERVER = os.environ.get('MAIL_SERVER')
MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true'
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
GOOGLE_CLIENT_ID=os.environ.get('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET=os.environ.get('GOOGLE_CLIENT_SECRET')





from flask_dance.contrib.google import make_google_blueprint
from flask import Blueprint

google_bp=Blueprint('google',__name__)



google_bp = make_google_blueprint(client_id=GOOGLE_CLIENT_ID,
                                   client_secret=GOOGLE_CLIENT_SECRET,
                                   scope=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
                                   redirect_url="https://127.0.0.1:5000/google/authorized"
                                   

                                   )

