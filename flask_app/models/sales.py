from flask_app import db
from sqlalchemy.orm import backref, relationship
from datetime import datetime


class Products(db.Model):

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable = False, unique=True)
    lead_time_days= db.Column(db.Integer(), nullable = False)
    pcs_for_box = db.Column(db.Integer(), nullable = False)
    price_for_box = db.Column(db.Float, nullable = False)
    prod_type = db.Column(db.String)


    def __repr__(self):
        return f"품번:{self.id}, 품명:{self.name}, 제품타입:{self.prod_type}, 생산소요일:{self.lead_time_days}, 박스당 {self.pcs_for_box} 개입, 가격(박스당): {self.price_for_box}"


class Order(db.Model):

    id = db.Column(db.Integer(), primary_key = True)
    date_of_request = db.Column(db.DateTime(), default=datetime.today())
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id', ondelete="CASCADE"))
    status = db.Column(db.Integer, default = 0) #0:접수 1:생산중 2:배송중 4:완료 
    lading_number = db.Column(db.Integer(), default = None)

    def __repr__(self):
        return f"""
        오더번호: {self.id},
        주문일자: {self.date_of_request},
        주문자(ID): {self.contact_id},
        송장번호: {self.lading_number}
        """

#Order - Products 간 many to many 관계 설정
class OrderItems(db.Model):

    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), primary_key = True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key = True)
    product_qty = db.Column(db.Integer, nullable = False)

    def __repr__(self):
        return f"오더번호: {self.order_id}, 품번: {self.product_id}, 수량{self.product_qty}"
        






# products_order = db.Table(
#     'products_order',
#     db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
#     db.Column('products_id', db.Integer, db.ForeignKey('products.id'), primary_key=True)
# )
# orders = db.relationship('Order', secondary = products_order, backref=db.backref('products')) 

# 다대다 관계 설정 - ref. https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/?highlight=type
# 공식문서 가이드대로 다대다 Table을 db.Table() 방식으로 생성, 지정해주려고 하였으나
# 두 외부키 외에 추가 컬럼 생성 및 쿼리 중 인스턴스 추가 등이 어려워 OrderItems 클래스(테이블)을 생성해주는 것으로 대체하였습니다.
