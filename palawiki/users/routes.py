from flask import (render_template, redirect, url_for, 
                   flash, request, abort, Blueprint)
from flask_login import login_user, current_user, logout_user, login_required 
from palawiki import db, bcrypt
from palawiki.models import User, Champion
from palawiki.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                            RequestResetForm, ResetPasswordForm)
from palawiki.users.utilities import send_reset_email

users = Blueprint('users', __name__)


@users.route("/user/<string:username>")
def user_posts(username):
  page = request.args.get('page', 1, type=int)
  user = User.query.filter_by(username=username).first_or_404()
  posts = Champion.query.filter_by(author=user)\
      .order_by(Champion.name.asc())\
      .paginate(page=page, per_page=4)
  return render_template('user_posts.html', title='Champions List', posts=posts, user=user)


@users.route("/register", methods=['GET', 'POST'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('main.home'))
  form = RegistrationForm()
  if form.validate_on_submit():
    hashed_password = bcrypt.generate_password_hash(
        form.password.data).decode('utf-8')
    user = User(username=form.username.data,
                email=form.email.data, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    flash(f'Account has been created! You are now able to log in.', 'success')
    return redirect(url_for('users.login'))
  return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('main.home'))
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    if user and bcrypt.check_password_hash(user.password, form.password.data):
      login_user(user, remember=form.remember.data)
      next_page = request.args.get('next')
      return redirect(next_page) if next_page else redirect(url_for('main.home'))
    else:
      flash('Login unsuccessful. Please check email and password', 'danger')
  return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
  logout_user()
  return redirect(url_for('main.home'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
  user = User.query.get_or_404(current_user.id)
  form = UpdateAccountForm()
  if form.validate_on_submit():
    current_user.username = form.username.data
    current_user.email = form.email.data
    current_user.image_file = form.picture_link.data
    db.session.commit()
    flash('Your account info has been updated.', 'success')
    return redirect(url_for('users.account'))
  elif request.method == 'GET':
    form.username.data = current_user.username
    form.email.data = current_user.email
    form.picture_link.data = current_user.image_file
  return render_template('account.html', title='Account', form=form, user=user)


@users.route("/account/<int:user_id>", methods=['GET', 'POST'])
@login_required
def delete_account(user_id):
  user = User.query.get_or_404(user_id)
  logout_user()
  db.session.delete(user)
  db.session.commit()
  flash('The user has been deleted!', 'success')
  return redirect(url_for('main.home'))


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
  if current_user.is_authenticated:
    return redirect(url_for('main.home'))
  form = RequestResetForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    send_reset_email(user)
    flash('An email has been sent to reset your password.', 'info')
    return redirect(url_for('users.login'))
  return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
  if current_user.is_authenticated:
    return redirect(url_for('main.home'))
  user = User.verify_reset_token(token)
  if user is None:
    flash('That is an expired or invalid token', 'warning')
    return redirect(url_for('users.reset_request'))
  form = ResetPasswordForm()
  if form.validate_on_submit():
    hashed_password = bcrypt.generate_password_hash(
        form.password.data).decode('utf-8')
    user.password = hashed_password
    db.session.commit()
    flash(f'Password has been updated! You are now able to log in.', 'success')
    return redirect(url_for('users.login'))
  return render_template('reset_token.html', title='Reset Password', form=form)
