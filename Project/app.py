from flask import Flask,redirect,url_for
from models import db,ADMIN,User,Product
from sqlalchemy.orm import Session
from Blueprints.admin_user_route import auth_bp
from Blueprints.API_route import api_bp,ProductResource
from Blueprints.views import page_bp
from Blueprints.email import email_bp
from config import google_bp
from flask_bcrypt import Bcrypt
from flask_admin import Admin,AdminIndexView
from flask_admin.menu import MenuLink
from flask_admin.contrib.sqla import ModelView
from flask_admin.form.upload import ImageUploadField
from flask_login import LoginManager,current_user
from flask_migrate import Migrate
from dotenv import load_dotenv  # type: ignore
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail,Message # type: ignore
from flask_restful import Api # type: ignore 
from config import SECRET_KEY



app=Flask(__name__,template_folder='templates')
app.config.from_pyfile('config.py')
migrate=Migrate(app,db)


app.register_blueprint(auth_bp)
app.register_blueprint(api_bp)
app.register_blueprint(page_bp)
app.register_blueprint(email_bp)
app.register_blueprint(google_bp)

load_dotenv()

bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view = 'auth.user_login'
db.init_app(app)

mail=Mail(app)
mail.init_app(app)
api=Api(app)
api.add_resource(ProductResource, '/products')




def send_email(subject, sender, recipients, body):
    with email_bp.app_context():
        msg = Message(subject, sender=sender, recipients=recipients)
        msg.body = body
        mail.send(msg)

serializer=URLSafeTimedSerializer(SECRET_KEY)



def run_export_product_data():
    from export_data import export_product_data
    export_product_data()  


def run_import_product_data():
    from export_data import import_product_data
    import_product_data() 

def run_export_user_data():
    from export_data import export_user_data
    export_user_data()    

def run_import_user_data():
    from export_data import import_user_data
    import_user_data() 



@login_manager.user_loader
def load_user(user_id):
    session=Session(bind=db.engine)

    try:
        user = session.get(ADMIN, int(user_id)) or session.get(User, int(user_id))
        return user
    finally:
        session.close()


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin
            
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.admin_login'))

admin = Admin(app, index_view=MyAdminIndexView())
admin.add_link(MenuLink(name='Exit', url='/admin_logout'))

class SelfAdminView(ModelView):
    column_list = ( 'username', 'password', 'email')
    form_columns = ( 'username', 'password', 'email')

admin.add_view(SelfAdminView(ADMIN, db.session,category='Admin', name='Admin Users', endpoint='self_admin', url='self_admin'))

class ProductAdminView(ModelView):
    form_extra_fields = {
         'picture': ImageUploadField('Picture',base_path='Project/static/images/',url_relative_path='images/')
         }
     
    column_list = ('category','picture', 'name', 'quantity','description', 'price', 'rate','created_at')
    form_columns = ('category','picture', 'name', 'quantity','description', 'price', 'rate','created_at')


admin.add_view(ProductAdminView(Product, db.session))

class UserAdminView(ModelView):
    column_list = ( 'username', 'password', 'email')
    form_columns = ( 'username', 'password', 'email')

admin.add_view(UserAdminView(User, db.session))



if __name__=='__main__':
    with app.app_context():
        run_import_user_data()
        db.create_all()
        db.session.close()
        
    app.run(debug=True)

#  ssl_context=('C:\\SSL_cert\\cert.pem', 'C:\\SSL_key\\key.pem'),

#   CODE-Y RUN ANELU HAMAR

#   cd C:\Users\Dex\Desktop\project    HAMAKARGCHUM FILE-I TEXY
#   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
#   venv\Scripts\activate   VIRTUAL ENVIROMENTI AKTIVACUM
#   python C:\Users\Dex\Desktop\project\Project\app.py    HAMAKARGCHUM FILE-I TEXY
#   Ctr + c  RUNY DADARACNELU HAMAR
#   deactivate   VIRTUAL ENVIROMENTI APAKTIVACUM
#   exit FILEIC DURS GALU HAMAR
