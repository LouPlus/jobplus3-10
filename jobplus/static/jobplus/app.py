from flask import Flask,render_template
from jobplus.config import configs
from simpledu.models import db,User,Company,Job

def create_app(config):

    app=Flask(__name__)
    app.config.from_object(configs.get(config))

    db.init_app(app)

    @app.route('/')
    def index():
        companys=Company.query.all()
        return render_template('index.html',companys=companys)
    @app.route('/admin')
    def admin_index():
        return 'admin'

    return app
