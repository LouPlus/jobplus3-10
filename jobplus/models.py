from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash

db=SQLAlchemy()

class Base(db.Model):
    __abstract__=True

    created_at=db.Column(db.DateTime,default=datetime.utcnow)
    updated_at=db.Column(
            db.DateTime,default=datetime.utcnow,onupdate=datetime.utcnow
            )

class User(Base,UserMixin):
    __tablename__='user'

    ROLE_USER=10
    ROLE_COMPANY=20
    ROLE_ADMIN=30

    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(
            db.String(32),unique=True,index=True,nullable=False)
    email=db.Column(db.String(64),unique=True,index=True,nullable=False)
    _password=db.Column('password',db.String(256),nullable=False)
    role=db.Column(db.SmallInteger,default=ROLE_USER)
        
    status=db.Column(db.SmallInteger,default=1)
    #用户上传的简历
    resume=db.Column(db.String(64))

    def __reper__(self):
        return '<User:{}>'.format(self.username)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self,orig_password):
        self._password=generate_password_hash(orig_password)

    def check_password(self,password):
        return check_password_hash(self._password,password)

    @property
    def is_admin(self):
        return self.role==self.ROLE_ADMIN

    @property
    def is_company(self):
        return self.role==self.ROLE_COMPANY

    @property
    def is_enable(self):
        return self.status==1


class Company(Base,UserMixin):
    __tablename__='company'
    
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    name=db.Column(db.String(32),unique=True,index=True,nullable=False)
    location=db.Column(db.String(32),default='中国')
    intro=db.Column(db.String(128),default='It has nothing to say')
    description=db.Column(db.String(128),default='It  has nothing to say')
    website=db.Column(db.String(256))
    
    profile=db.relationship(
            'User',backref=db.backref('company',uselist=False),uselist=False)
    logo_url=db.Column(
            db.String(256)
            )

    def __repr__(self):
        return '<Company:{}'.format(self.name)

#求职人与工作的表联系
assoc_job_user=db.Table(
        'assoc_job_user',
        db.Column('user_id',db.Integer,
            db.ForeignKey('user.id',ondelete='CASCADE')),
        db.Column('job_id',db.Integer,
            db.ForeignKey('job.id',ondelete='CASCADE'))

        )

class Job(Base,UserMixin):
    __tablename__='job'

    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(32),nullable=False)
    salary=db.Column(db.String(32),nullable=False)
    #职位要求，经验要求，学历要求
    #requirements=db.Column(db.String(128),nullabel=False)
    experience=db.Column(db.String(128),nullable=False)
    degree=db.Column(db.String(32))

    address=db.Column(db.String(32))
    description=db.Column(db.String(256),nullable=False)
    status=db.Column(db.SmallInteger,default=1)
    company_id=db.Column(db.Integer,db.ForeignKey('company.id'))
    
    company=db.relationship(
        'Company',backref=db.backref('job',uselist=False),uselist=False)

#求职者与工作的表关系
    interviewee=db.relationship(
        'User',
        secondary=assoc_job_user,
        backref=db.backref('send',uselist=False),
        uselist=False)

    def __repr__(self):
        return '<Job:{}>'.format(self.name)

    @property
    def is_enable(self):
        return self.status==1

