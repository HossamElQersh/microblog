from flask import render_template, request, redirect, flash, url_for
from werkzeug.urls import url_parse
from app.auth import bp
from flask_login import current_user, login_user, logout_user
from flask_babel import _
from app import db
from app.auth.email import send_password_reset_email
from app.auth.forms import RegistrationForm, LoginForm, ResetPasswordRequestForm, ResetPasswordForm
from app.models import User


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Register <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(_("Congratulations you are a member in our microblog !!"))
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form, title=_('Register'))


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> login / logout <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(password=form.password.data):
            flash(_("Invalid username or password"))
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html', title=_('Login'), form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Password Reset <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash(_('Check your email for the instructions to reset your password'))
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html',
                           title=_('Reset Password'), form=form)


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authdicated():
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_passowrd(form.password.data)
        db.session.commit()
        flash(_('Password Changed !'))
        redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html', form=form)
