from sqlalchemy.orm import relationship, backref
from flask_app import db
from datetime import datetime


class Company(db.Model):


    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable = False, unique=True)
    location = db.Column(db.Text())

    employee = db.relationship('Contact', backref = 'company', cascade= 'all, delete')

    def __repr__(self):
        return f"ID:{self.id}, 회사명:{self.name}, 위치:{self.location}"



class Contact(db.Model):
 

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable = False)
    email = db.Column(db.String(), nullable = False, unique=True)
    tel = db.Column(db.String(), nullable = False)
    company_id = db.Column(db.Integer(), db.ForeignKey('company.id', ondelete='CASCADE'))


    ordering = relationship('Order', backref='contact')

    def __repr__(self):
        return f"ID:{self.id}, 성함:{self.name}, 이메일:{self.email}, 전화번호:{self.tel}"

