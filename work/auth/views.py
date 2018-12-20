from flask import render_template, redirect, url_for, request
from flask_login import LoginManager, login_required, login_user, logout_user
from forms.signin import SignInForm
from forms.signin import RegisterForm
from forms.signin import SignUpForm
from flask import current_app
from blueprints import auth
from models import User
from forms.watermark import WatermarkForm
from extentions import db
from extentions import login_manager
from flask import flash
from werkzeug.security import generate_password_hash
import os
from image import embed_watermark
from audio import lsb_watermark
from video import embed_video
from flask import request,Response
from flask import make_response,send_from_directory
@login_manager.user_loader
def load_user(userid):
    return User.query.filter(User.id == userid).first()

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = SignInForm()
    if form.validate_on_submit():
        print('test1')
        user = User.query.filter_by(email=form.email.data).first_or_404()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            print('test3')
            next = request.args.get('next')
            return redirect(next or url_for('home.index'))
        else:
            flash('password worry')
            return redirect(url_for('auth.login'))
    return render_template("auth/login.html",form=form)

@auth.route('/register',methods=['GET','POST'])
def register():
    form=RegisterForm()
    if form.validate_on_submit():
        print('ttt')
        users=User.query.filter_by(email=form.email.data).all()
        if not len(users):
            name=form.username.data
            email=form.email.data
            password=form.password.data
            #password=generate_password_hash(form.password.data)
            print('woc')
            insertuser=User(username=name,email=email,_password=password)
            db.session.add(insertuser)
            db.session.commit()
            flash('success,click login')
            return redirect(url_for('auth.login'))
        else:  
            flash('please register another email account')
            return redirect(url_for('auth.register'))
    return render_template('auth/register.html',form=form,message='register please')
    

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return 'Logged out successfully!'

@auth.route('/image',methods=['GET','POST'])
@login_required
def image():
    global IMAGE_PATH
    form = WatermarkForm()
    if form.validate_on_submit():
        f = request.files['file']
        save_path = os.path.join(current_app.instance_path, 'upload', f.filename)
        f.save(save_path)
        IMAGE_PATH = save_path
        if len(IMAGE_PATH)==0:
            return redirect(url_for('auth.image'))
        else:
            watermark_string = form.watermark.data
            temp_file_path = os.path.join(current_app.instance_path, 'temp', 'temp.jpg')
            print(temp_file_path)
            embed_watermark(IMAGE_PATH, watermark_string, temp_file_path)
            print('ok')
            return redirect(url_for('auth.image_get',filename='temp.jpg'))       
    #return redirect(url_for('image'))
    return render_template('auth/image.html', form=form)

@auth.route("/image_get/<filename>",methods=['GET']) 
def image_get(filename): 
 #要知道2个参数, 第1个参数是本地目录的path, 第2个参数是文件名(带扩展名)
    directory = os.path.join(current_app.instance_path, 'temp')          # 假设在当前目录
    response = make_response(send_from_directory(directory, filename, as_attachment=True))
    response.headers["Content-Disposition"] = "attachment; filename={}".format(filename.encode().decode('latin-1'))
    return response
    
    

@auth.route('/audio',methods=['GET','POST'])
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
            return redirect(url_for('auth.audio'))
        else:
            watermark_string = form.watermark.data
            temp_file_path = os.path.join(current_app.instance_path, 'temp', 'temp.wav')
            lsb_watermark(AUDIO_PATH, watermark_string, temp_file_path)
            return redirect(url_for('auth.audio_get',filename='temp.wav'))
    return render_template('auth/audio.html',form=form)

@auth.route("/audio_get/<filename>",methods=['GET']) 
def audio_get(filename): 
 #要知道2个参数, 第1个参数是本地目录的path, 第2个参数是文件名(带扩展名)
    directory = os.path.join(current_app.instance_path, 'temp')          # 假设在当前目录
    response = make_response(send_from_directory(directory, filename, as_attachment=True))
    response.headers["Content-Disposition"] = "attachment; filename={}".format(filename.encode().decode('latin-1'))
    return response

@auth.route('/video',methods=['GET','POST'])
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
            return redirect(url_for('auth.video'))
        else:
            watermark_string = form.watermark.data
            temp_file_path = os.path.join(current_app.instance_path, 'temp', 'temp.mp4')
            embed_video(VIDEO_PATH, watermark_string, temp_file_path)
            return redirect(url_for('auth.video_get',filename='temp.mp4'))
    return render_template('auth/video.html',form=form)

@auth.route("/video_get/<filename>",methods=['GET']) 
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

