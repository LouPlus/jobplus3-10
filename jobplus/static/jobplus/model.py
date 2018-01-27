from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy(app)

class User(db.Model):
    __tablename__='user'

    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(
            db.String(32),unique=True,index=True,nullable=False)
    email=db.Column(db.String(64),unique=True,index=True,nullable=False)
    #   role=db.Column(db.SmallInteger,default=ROLE_USER)
    status=db.Column(db.SmallInteger,default=1)

    created_at=db.Column(db.DateTime,default=datetime.utcnow)
    updated_at=db.Column(
            db.DateTime,default=datetime.utcnow,onupdate=datetime.utcnow
            )

class Company(db.Model):
    __tablename__='company'
    
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    name=db.Column(db.String(32),unique=True,index=True,nullable=False)
    location=db.Column(db.String(32),default='中国')
    intro=db.Column(db.String(128),default='It has nothing to say')
    description=db.Column(db.String(128),default='It  has nothing to say')
    website=db.Column(db.String(256))

class Job(db.Model):
    __tablename__='job'

    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(32),nullable=False)
    salary=db.Column(db.String(32),nullable=False)
    requirements=db.Column(db.String(128),nullable=False)
    description=db.Column(db.String(256),nullable=False)
    status=db.Column(db.SmallInteger,default=1)
    company_id=db.Column(db.Integer,db.ForeignKey('company.id'))


