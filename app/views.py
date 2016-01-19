#!/usr/bin/python
from flask import Flask,render_template,request,session,flash,redirect,url_for,g
#from flask import *
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager,login_user,logout_user,current_user,login_required
from app import app,db,lm
from app.models import User,RepoInfo
bootstrap=Bootstrap(app)

@lm.user_loader
def load_user(uid):
    return User.query.get(int(uid))

@app.before_request
def before_request():
    g.user = current_user




@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('home.html')

@app.route('/add/repos',methods=['GET','POST'])
@login_required
def add_repos():
    from forms import ReposForm
    form=ReposForm()
    if request.method=='GET':
        return render_template('add-repo.html',form=form)
    if form.validate_on_submit():
        repo=RepoInfo.query.filter_by(repo_name=form.repo_name.data.lower()).first()
        if repo is not None:
            form.repo_name.errors.append("the repo has exist !!")
            return render_template('add-repo.html',form=form)
        repo=RepoInfo(form.repo_name.data,form.repo_address.data,form.repo_user.data,form.repo_passwd.data,form.local_checkout_path.data,form.repo_type.data,form.remote_deploy_path.data)
        db.session.add(repo)
        db.session.commit()
        return redirect(url_for('index')) 
    else:
        return render_template('add-repo.html',form=form,failed_auth=True) 
    return render_template('add-repo.html',form=form)








@app.route('/login',methods=['GET','POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    from forms import LoginForm
    form=LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and user.check_password(form.password.data):
            session['email']=form.email.data
            login_user(user)
            return redirect(url_for('index'))
        else:
            return render_template('login.html',form=form,failed_auth=True)
    return render_template('login.html',form=form)

