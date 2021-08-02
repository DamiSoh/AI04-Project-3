from datetime import date
from flask import Blueprint, redirect, render_template, request, flash
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from flask_app.models import customer, sales
from flask_app import db
from flask_app.service.recommend import prediction
import datetime
import pandas as pd


##===========================Home 입니다===========================##

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')



###===========================USER 드롭다운 입니다===========================###
###------------------------OrderRequest 페이지 입니다------------------------###


@bp.route('/user', methods = ["GET"])
def new_form():
    product_list = db.session.query(sales.Products).all()
    return render_template('form_.html', product_list = product_list)

@bp.route('/user', methods = ['POST'])
def new_form_fillout():

    company = request.form["company"]
    location = request.form["location"]
    contact_name = request.form["contact_name"]
    email = request.form["email"]
    mobile = request.form["mobile"]
    item_id = request.form["item_id"]
    qty = request.form["qty"]

    #미등록 업체 확인 및 등록
    if db.session.query(customer.Company).filter(customer.Company.name == company).first() == None:
        new = customer.Company()
        new.name = str(company)
        new.location = str(location)
        db.session.add(new)
        db.session.commit()

    else:
        pass

    #미등록 담당자 확인 및 등록
    if db.session.query(customer.Contact).filter(customer.Contact.name == contact_name).first() == None:
        contact_new = customer.Contact()
        contact_new.name = str(contact_name)
        contact_new.email = str(email)
        contact_new.tel = str(mobile)
        find_id = customer.Company.query.filter_by(name=str(company)).first()
        contact_new.company_id = int(find_id.id)
        db.session.add(contact_new)
        db.session.commit()

    else:
        pass

    #오더 등록
    new_order = sales.Order()
    contact_id = customer.Contact.query.filter_by(email=str(email)).first()
    new_order.contact_id = int(contact_id.id)
    db.session.add(new_order)
    db.session.commit()

    new_order_items = sales.OrderItems()

    id_find = sales.Order.query.order_by(sales.Order.id.desc()).first()
    new_order_items.order_id = int(id_find.id)

    new_order_items.product_id = int(item_id)
    new_order_items.product_qty = int(qty)

    db.session.add(new_order_items)
    db.session.commit()

    return "접수되었습니다. 감사합니다."





###------------------------상품 Recommend 페이지 입니다------------------------###


@bp.route('/user/recommend', methods=['GET'])
def recommend_index():
    return render_template('recommend.html')

@bp.route('/user/recommend', methods=['POST'])
def recommend():
    cu_age = str(request.form['age'])
    cu_sex = str(request.form['sex'])
    cu_season = str(request.form['season'])

    cu_spec = [cu_age, cu_sex, cu_season]
    cu_rec_type = prediction(cu_spec)

    rec_list = sales.Products.query.filter_by(prod_type = cu_rec_type).\
                order_by(sales.Products.id.desc()).\
                all()
    return render_template('recommend.html', cu_rec_type=cu_rec_type, rec_list=rec_list)



###------------------------My page 페이지 입니다------------------------###


@bp.route('/user/my_page', methods = ["GET"])
def my_order():
    return render_template('my_page.html')


@bp.route('/user/my_page', methods = ["POST"])
def my_order_details():

    email_ = request.form["email_"]
    search_id = customer.Contact.query.filter_by(email=str(email_)).first()

    if not search_id:
        flash("해당 이메일로 조회되는 주문이 없습니다.")
        return render_template('my_page.html')

    else:
        search_id = int(search_id.id)
        
        #접수된 주문
        order_list_0 = sales.Order.query.filter_by(contact_id=search_id).\
            filter_by(status = 0).all()
        #생산중 주문    
        order_list_1 = sales.Order.query.filter_by(contact_id=search_id).\
            filter_by(status = 1).all()
        #발송 완료된 주문    
        order_list_2 = sales.Order.query.filter_by(contact_id=search_id).\
            filter_by(status = 2).all() 
        #전체 주문 상세내역 - 최근 오더넘버 먼저 Display
        details = db.session.query(sales.Order.id, customer.Contact.name, sales.Order.date_of_request, sales.Products.name, sales.Products.price_for_box,  sales.OrderItems.product_qty,).\
                join(sales.OrderItems, sales.Order.id == sales.OrderItems.order_id).\
                join(sales.Products, sales.OrderItems.product_id == sales.Products.id ).\
                join(customer.Contact, sales.Order.contact_id == customer.Contact.id).\
                filter(customer.Contact.id == search_id).\
                order_by(sales.Order.id.desc()).\
                all()

        all_details = []
        column = ['오더번호', '주문인(성함)', '주문일자', '품명', '단가', '주문수량', '총금액']

        for tups in details:
            tups = list(tups)
            tups[2] = tups[2].strftime('%Y/%m/%d')
            total = int(tups[4]) * float(tups[5])
            tups.append(total)
            all_details.append(tups)

        df = pd.DataFrame(all_details, columns = column)
        df = df.to_html(justify="justify-all", index=False, bold_rows=True, border = 1)

        return render_template('my_page.html', order_list_0 = order_list_0, order_list_1 = order_list_1, order_list_2 = order_list_2, df=df)

    
