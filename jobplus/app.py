from flask import Flask,render_template
from jobplus.config import configs
from jobplus.models import db,User,Company,Job

def register_blueprints(app):
    from .handlers import front,company,admin,user,job
    app.register_blueprint(front)
    app.register_blueprint(company)
    app.register_blueprint(admin)
    app.register_blueprint(user)
    app.register_blueprint(job)

def create_app(config):

    app=Flask(__name__)
    app.config.from_object(configs.get(config))

    db.init_app(app)

    register_blueprints(app)
    
    return app
"""
    @app.route('/')
    def index():
        companys=Company.query.all()
        return render_template('index.html',companys=companys)

    @app.route('/admin')
    def admin_index():
        return 'admin'
"""
