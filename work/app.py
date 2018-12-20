from flask import render_template, redirect, url_for, request,Flask,flash
from forms.signin import SignInForm,RegisterForm
from templates import AdminLTE
from flask_wtf.csrf import CSRFProtect
from forms.watermark import WatermarkForm
from flask_login import LoginManager, login_required, login_user, logout_user
from flask import request,  current_app, Response
from video import embed_video
from image import embed_watermark
from audio import lsb_watermark
from flask import make_response,send_from_directory
import os
from flask_sqlalchemy import SQLAlchemy
from models import User
from database import create_app
VIDEO_PATH = ''
IMAGE_PATH = ''
AUDIO_PATH = ''
csrf = CSRFProtect()
app = create_app()
AdminLTE(app)
app.secret_key = 'LearnFlaskTheHardWay2017'
csrf.init_app(app)

# Add LoginManager
login_manager = LoginManager()
login_manager.session_protection = 'AdminPassword4Me'
login_manager.login_view = 'login'
login_manager.login_message = 'Unauthorized User'
login_manager.login_message_category = "info"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
  return User.query.get(int(userid))

@app.route('/')
def index():
    name=None
    message='please login or register before use this function'    
    return render_template('index.html',name=name,message=message)

# @app.route('/index/<username>')
# def index2():
#     name=
#     form=SignInForm()
#     return render_template('index2.html',name=name)


# @app.route('/login', methods=['GET'])
# def signin():
#     form = SignInForm()
#     return render_template('login.html', form=form)

# @app.route('/login', methods=['POST'])
# def login():
#     form = SignInForm()
#     if form.validate_on_submit():
#         if form.email.data=='admin' and form.password.data=='111':
#             return render_template('index.html', name=form.username.data)
#         else:
#             return render_template('login.html', form=form, message='password and user name mismatch, login failed')
#     else:
#         return render_template('login.html', form=form, message='invalid form fields, try again')

@app.route('/register',methods=['GET','POST'])
def register():
    form=RegisterForm()
    if form.validate_on_submit():
        name=form.username.data
        id=form.id.data
        email=form.email.data
        password=form.password.data
        insertuser=User(username=name,id=id,email=email,password=password)
        db.session.add(insertuser)
        db.session.commit()
        return render_template('index.html',name=name,message='success,click login')
    else:  
        return render_template('register.html',form=form,message='register please')
    
@app.route('/login',methods=['GET','POST'])
def login():
    form=SignInForm()
    if form.validate_on_submit():
       name=form.username.data
       user=User.query.filter_by(username=name).first()
       if user is not None and user.verify_password(form.password.data):
            login_user(user)
            next = request.args.get('next')
            return redirect(next or url_for('index'))
       else:
            return render_template('login.html',form=form)

@app.route('/image',methods=['GET','POST'])
# @login_required

def image():
    global IMAGE_PATH
    form = WatermarkForm()
    if form.validate_on_submit():
        f = request.files['file']
        save_path = os.path.join(current_app.instance_path, 'upload', f.filename)
        f.save(save_path)
        IMAGE_PATH = save_path
        if len(IMAGE_PATH)==0:
            return redirect(url_for('image'))
        else:
            watermark_string = form.watermark.data
            temp_file_path = os.path.join(current_app.instance_path, 'temp', 'temp.jpg')
            print(temp_file_path)
            embed_watermark(IMAGE_PATH, watermark_string, temp_file_path)
            print('ok')
            return redirect(url_for('image_get',filename='temp.jpg'))       
    #return redirect(url_for('image'))
    return render_template('image.html', form=form)

@app.route("/image_get/<filename>",methods=['GET']) 
def image_get(filename): 
 #要知道2个参数, 第1个参数是本地目录的path, 第2个参数是文件名(带扩展名)
    directory = os.path.join(current_app.instance_path, 'temp')          # 假设在当前目录
    response = make_response(send_from_directory(directory, filename, as_attachment=True))
    response.headers["Content-Disposition"] = "attachment; filename={}".format(filename.encode().decode('latin-1'))
    return response
    
    

@app.route('/audio',methods=['GET','POST'])
# @login_required
def audio():
    form=WatermarkForm()
    global AUDIO_PATH
    if form.validate_on_submit():
        f = request.files['file']
        save_path = os.path.join(current_app.instance_path, 'upload', f.filename)
        f.save(save_path)
        AUDIO_PATH = save_path
        if len(AUDIO_PATH)==0:
            return redirect(url_for('audio'))
        else:
            watermark_string = form.watermark.data
            temp_file_path = os.path.join(current_app.instance_path, 'temp', 'temp.wav')
            lsb_watermark(AUDIO_PATH, watermark_string, temp_file_path)
            return redirect(url_for('audio_get',filename='temp.wav'))
    return render_template('audio.html',form=form)

@app.route("/audio_get/<filename>",methods=['GET']) 
def audio_get(filename): 
 #要知道2个参数, 第1个参数是本地目录的path, 第2个参数是文件名(带扩展名)
    directory = os.path.join(current_app.instance_path, 'temp')          # 假设在当前目录
    response = make_response(send_from_directory(directory, filename, as_attachment=True))
    response.headers["Content-Disposition"] = "attachment; filename={}".format(filename.encode().decode('latin-1'))
    return response

@app.route('/video',methods=['GET','POST'])
# @login_required
def video():
    form=WatermarkForm()
    global VIDEO_PATH
    if form.validate_on_submit():
        f = request.files['file']
        save_path = os.path.join(current_app.instance_path, 'upload', f.filename)
        f.save(save_path)
        VIDEO_PATH = save_path
        if len(VIDEO_PATH)==0:
            return redirect(url_for('video'))
        else:
            watermark_string = form.watermark.data
            temp_file_path = os.path.join(current_app.instance_path, 'temp', 'temp.mp4')
            embed_video(VIDEO_PATH, watermark_string, temp_file_path)
            return redirect(url_for('video_get',filename='temp.mp4'))
    return render_template('video.html',form=form)

@app.route("/video_get/<filename>",methods=['GET']) 
def video_get(filename): 
 #要知道2个参数, 第1个参数是本地目录的path, 第2个参数是文件名(带扩展名)
    directory = os.path.join(current_app.instance_path, 'temp')          # 假设在当前目录
    response = make_response(send_from_directory(directory, filename, as_attachment=True))
    response.headers["Content-Disposition"] = "attachment; filename={}".format(filename.encode().decode('latin-1'))
    return response
# @app.route('/signin', methods=['GET', 'POST'])
# def signin():
#     form = SignInForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         if user is not None and user.verify_password(form.password.data):
#             login_user(user)

#             next = request.args.get('next')
#             return redirect(next or url_for('watermark'))

#     return render_template('signin.html', form=form)


# @app.route('/upload', methods=['POST'])
# def upload():
#     f = request.files['file']
#     save_path = os.path.join(app.instance_path, 'upload', f.filename)
#     f.save(save_path)

#     return redirect(url_for('watermark'))


# @app.route('/watermark', methods=['GET', 'POST'])
# @login_required
# def watermark():
#     form = WatermarkForm()
#     if form.validate_on_submit():
#         print(form.watermark.data)
#         return redirect(url_for('watermark'))

#     return render_template('watermark.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)

    