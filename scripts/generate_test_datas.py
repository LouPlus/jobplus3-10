"""
根据爬取的数据，生成公司用户，公司和职位信息；
同一公司发布两个以上职位时，存在不同的用户，后续再修改
"""
import os 
import json
from random import randint
from faker import Faker
from jobplus.models import db,User,Company,Job

fake=Faker()

def iter_fake_data():
    with open(os.path.join(os.path.dirname(__file__),'..','datas','job.json')) as f:
        job_data=json.load(f)
   
    usernum=1000
    for job in job_data:
        job_company=job['company_name']
        if Company.query.filter_by(name=job_company).first() is None:
            user=User(
                username='company'+str(usernum),
                email='company'+str(usernum)+'@qq.com',
                password='aaaaaa',
                role=User.ROLE_COMPANY
                )
            usernum=usernum+1

            company=Company(
                name=job['company_name'],
                location=job['location'],
                logo_url=job['img_url'],
                description=fake.text(),
                website=fake.url,
                #公司用户数据
                #profile=user()
                )

        job=Job(
                name=job['name'],
                salary=job['salary'],
                experience=job['experience'],
                degree=job['degree'],
                address=job['location'],#location as address
                description=fake.text(),
                company=company)

        try:
            db.session.add(user)
            db.session.add(company)
            db.session.add(job)
        except Exception as e:
            print(e)
            db.session.rollback()
    try:
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
