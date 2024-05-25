from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime,timezone
from flask_login import UserMixin 

db=SQLAlchemy()



class ADMIN(db.Model,UserMixin):
    __tablename__='admin'

    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(60),nullable=False)
    password=db.Column(db.String(60),nullable=True)
    email=db.Column(db.String(50),unique=True, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=True)


    def get_reset_token(self,expires_sec=3600):
        from app import serializer
        return serializer.dumps({'admin_id':self.id}, salt='reset_password')
    




class User(db.Model,UserMixin):
    __tablename__='user'

    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(60),nullable=False)
    password=db.Column(db.String(60),nullable=True)
    email=db.Column(db.String(60),unique=True, nullable=False)
    user_api=db.Column(db.String(60),nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)

    def get_reset_token(self,expires_sec=3600):
        from app import serializer
        return serializer.dumps({'user_id':self.id}, salt='reset_password')
    
    @staticmethod
    def verify_reset_token(token, expires_sec=3600):
        from app import serializer
        data = serializer.loads(token, salt='reset_password', max_age=expires_sec)
        if 'admin_id' in data:
            return ADMIN.query.get(data['admin_id'])
        elif 'user_id' in data:return User.query.get(data['user_id'])



class Product(db.Model):
    __tablename__='product'

    id=db.Column(db.Integer,primary_key=True)
    category=db.Column(db.String(60),nullable=False)
    picture=db.Column(db.String(60),nullable=False)
    name=db.Column(db.String(60),nullable=False)
    quantity=db.Column(db.Integer,nullable=False)
    description=db.Column(db.String(255),nullable=False)
    price=db.Column(db.Float,nullable=False)
    rate=db.Column(db.Float,nullable=False)
    created_at=db.Column(db.DateTime,default=datetime.now(timezone.utc))
    


   





