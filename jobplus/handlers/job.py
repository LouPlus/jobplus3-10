from flask import Blueprint,render_template,redirect,url_for,request,current_app,flash
from jobplus.models import Job,User,Company

job=Blueprint('job',__name__,url_prefix='/job')

@job.route('/')
def index():
    page=request.args.get('page',default=1,type=int)
#    INDEX_PER_PAGE=8 #默认显示的数量为8，一般在BaseConfig中设置
    pagination=Job.query.paginate(
            page=page,
            per_page=current_app.config['INDEX_PER_PAGE'],
            error_out=False)

    return render_template('job/job_list.html',pagination=pagination)
