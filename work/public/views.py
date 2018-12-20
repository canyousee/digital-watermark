# -*- coding: UTF-8 -*-
from flask import render_template, redirect, url_for, request

from blueprints import home

@home.route('/')
def index():
   name=None
   #message='please login or register before use this function'    
   return render_template("index.html",name=name)

   #return render_template('index.html',name=name,message=message)
# @home.route('/auth/register',methods=['GET','POST'])
# def register():
#     form=RegisterForm()
#     if form.validate_on_submit():
#         name=form.username.data
#         #id=form.id.data
#         email=form.email.data
#         password=form.password.data
#         insertuser=User(username=name,id=id,email=email,password=password)
#         db.session.add(insertuser)
#         db.session.commit()
#         return render_template('index.html',name=name,message='success,click login')
#     else:  
#         return render_template('register.html',form=form,message='register please')
   