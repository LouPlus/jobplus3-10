from flask import Blueprint,render_template
from jobplus.models import Company

front=Blueprint('front',__name__)
    
@front.route('/')
def index():
    companys=Company.query.all()
    return render_template('index.html',companys=companys)
