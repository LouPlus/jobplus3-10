from flask import Blueprint,render_template,redirect,url_for,flash
from jobplus.models import Company,User,Job
from jobplus.forms import UserRegisterForm,CompanyRegisterForm,LoginForm
from flask_login import login_user,logout_user,login_required

front=Blueprint('front',__name__)
    
@front.route('/')
def index():
#公司和职位列表（各8个，按时间排序）
#    companys=Company.query.all()
    jobs=Job.query.order_by(Job.updated_at.desc()).limit(8)
    companys=Company.query.order_by(Company.updated_at.desc()).limit(8)
    return render_template('index.html',jobs=jobs,companys=companys)

@front.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()

    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        login_user(user,form.remember_me.data)
        return redirect(url_for('.index'))

    return render_template('login.html',form=form)

@front.route('/user_register',methods=['GET','POST'])
def user_register():
#用户注册
    user_form=UserRegisterForm()
    if user_form.validate_on_submit():
        user_form.create_user()
        flash('注册成功，请登录！','success')
        return redirect(url_for('.login'))
    return render_template(
            'user_register.html',user_form=user_form)

@front.route('/company_register',methods=['GET','POST'])
def company_register():
#公司注册
    company_form=CompanyRegisterForm()
    user=User()
    role=user.ROLE_COMPANY
    if company_form.validate_on_submit():
        company_form.create_company(role)
        flash('注册成功，请登录！','success')
        return redirect(url_for('.login'))
    return render_template(
            'company_register.html',company_form=company_form)

#用户退出登录
@front.route('/logout')
@login_required
def logout():
    logout_user()
    flash('你已退出登录','success')
    return redirect(url_for('.index'))
