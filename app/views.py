from flask import render_template, flash, redirect
from flask.ext.login import login_user, logout_user, current_user, \
    login_required, session
from app import app, login_manager
from .forms import LoginForm
from user import User

@login_manager.user_loader
def load_user(id):
    return User.get(id)

@login_manager.unauthorized_handler
def unauthorized():
    return redirect('/login')

@app.route('/')
@login_required
def index():
    user = {'nickname': current_user.id}
    return render_template('index.html',
                           title='Home',
                           user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated():
        return  index()

    form = LoginForm()
    if form.validate_on_submit():
        u = form.username.data
        p = form.password.data

        user = User.get(u)
        if user and user.password == p:
            login_user(user)
            session['logged_in'] = True
            return redirect('/')

    return render_template('login.html',
                           title='Sign In',
                           form=form)

@app.route('/logout')
def logout():
    logout_user()
    session['logged_in'] = False
    return redirect('/login')