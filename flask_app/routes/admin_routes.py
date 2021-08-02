from datetime import date
from flask import Blueprint, redirect, render_template, request, flash
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from flask_app.models import customer, sales
from flask_app import db
import datetime

admin_bp = Blueprint('admin', __name__)


###===========================admin 드롭다운 입니다===========================###
###------------------------admin 페이지 입니다------------------------###


@admin_bp.route('/admin')
def admin():
    product_list = db.session.query(sales.Products).all()
    return render_template('admin.html', product_list = product_list)

@admin_bp.route('/admin', methods = ['POST'])
def prod_create():

    n_name = request.form["prod_name"]
    n_lead_time_days = request.form["prod_days"]
    n_pcs_for_box = request.form["prod_pcs"]
    n_price_for_box = request.form["prod_price"]
    n_prod_type = request.form["prod_type"]

    #품명이 사용 중인 경우 확인 
    if db.session.query(sales.Products).filter(sales.Products.name == str(n_name)).first():
        return "사용 중인 이름입니다."

    else:
        new_prod = sales.Products()
        new_prod.name = str(n_name)
        new_prod.lead_time_days = int(n_lead_time_days)
        new_prod.pcs_for_box = int(n_pcs_for_box)
        new_prod.price_for_box = float(n_price_for_box)
        new_prod.prod_type = str(n_prod_type)

        db.session.add(new_prod)
        db.session.commit()

        flash("등록이 완료되었습니다. 새로고침 후 판매품번을 확인하세요.")
        return render_template('admin.html')


###------------------------management 페이지 입니다------------------------###


@admin_bp.route('/admin/management', methods = ["GET"])
def awaiting():
    #접수된 주문
    order_list_0 = sales.Order.query.filter_by(status = 0).all()
    #생산중 주문    
    order_list_1 = sales.Order.query.filter_by(status = 1).all()
    #발송 완료된 주문    
    order_list_2 = sales.Order.query.filter_by(status = 2).all() 
    return render_template('admin_kanban.html', order_list_0=order_list_0, order_list_1=order_list_1, order_list_2=order_list_2)