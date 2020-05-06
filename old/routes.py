import secrets
from flask import render_template, redirect, url_for, flash, request, abort
from palawiki import app, db, bcrypt, mail
from palawiki.forms import (RegistrationForm, LoginForm, UpdateAccountForm, ChampionPost, PicturePost, UpdateChampion, 
                            UpdatePortait, RequestResetForm, ResetPasswordForm)
from palawiki.models import User, Champion, Pictures
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message


@app.route("/")
def home():
    return render_template('home.html', title='Home')

@app.route("/champions")
def championslist():
  page = request.args.get('page', 1, type=int)
  posts = Champion.query.order_by(Champion.name.asc()).paginate(page=page, per_page=4)
  return render_template('champion_list.html', title='Champions List', posts=posts)


@app.route("/champions/<int:champion_id>", methods=['GET', 'POST'])
def full_article(champion_id):
  post = Champion.query.get_or_404(champion_id)
  return render_template('full_article.html', title=post.name, post=post)


@app.route("/user/<string:username>")
def user_posts(username):
  page = request.args.get('page', 1, type=int)
  user = User.query.filter_by(username=username).first_or_404()
  posts = Champion.query.filter_by(author=user)\
      .order_by(Champion.name.asc())\
      .paginate(page=page, per_page=4)
  return render_template('user_posts.html', title='Champions List', posts=posts, user=user)

  
@app.route("/register", methods=['GET', 'POST'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('home'))
  form = RegistrationForm()
  if form.validate_on_submit():
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    user = User(username=form.username.data, email=form.email.data, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    flash(f'Account has been created! You are now able to log in.', 'success')
    return redirect(url_for('login'))
  return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('home'))
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    if user and bcrypt.check_password_hash(user.password, form.password.data):
      login_user(user, remember=form.remember.data)
      next_page = request.args.get('next')
      return redirect(next_page) if next_page else redirect(url_for('home'))
    else:
      flash('Login unsuccessful. Please check email and password', 'danger')
  return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
  logout_user()
  return redirect(url_for('home'))
  
  
@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
  form = UpdateAccountForm()
  if form.validate_on_submit():
    current_user.username = form.username.data
    current_user.email = form.email.data
    current_user.image_file = form.picture_link.data
    db.session.commit()
    flash('Your account info has been updated.', 'success')
    return redirect(url_for('account'))
  elif request.method == 'GET':
    form.username.data = current_user.username
    form.email.data = current_user.email
    form.picture_link.data = current_user.image_file
  return render_template('account.html', title='Account', form=form)


@app.route("/create", methods=['POST', 'GET'])
@login_required
def newpost():
  form = ChampionPost()
  if form.validate_on_submit():
    flash('Your post has been created successfully', 'success')
    post = Champion(name=form.name.data, title=form.title.data, role=form.role.data, hp=form.hp.data,
                    speed=form.speed.data, summary=form.summary.data, content=form.content.data, 
                    skill_1=form.skill_1.data, skill_2=form.skill_2.data, skill_3=form.skill_3.data, 
                    skill_4=form.skill_4.data, skill_5=form.skill_5.data, portait=form.portait.data,
                    author=current_user)
    db.session.add(post)
    db.session.commit()
    return redirect(url_for('championslist'))
  return render_template('new_entry.html', title='New Entry', form=form, legend='Create a new entry')


@app.route("/champions/<int:champion_id>/edit", methods=['GET', 'POST'])
@login_required
def edit(champion_id):
  post = Champion.query.get_or_404(champion_id)
  if post.author != current_user:
    abort(403)
  form = UpdateChampion()
  if form.validate_on_submit():
    post.name = form.name.data
    post.title = form.title.data
    post.role = form.role.data
    post.hp = form.hp.data
    post.speed = form.speed.data
    post.summary = form.summary.data
    post.content = form.content.data
    post.skill_1 = form.skill_1.data
    post.skill_2 = form.skill_2.data
    post.skill_3 = form.skill_3.data
    post.skill_4 = form.skill_4.data
    post.skill_5 = form.skill_5.data
    db.session.commit()
    flash('Your entry has been updated!', 'success')
    return redirect(url_for('full_article', champion_id=post.id))
  elif request.method == 'GET':
    form.name.data = post.name
    form.title.data = post.title
    form.role.data = post.role
    form.hp.data = post.hp
    form.speed.data = post.speed
    form.summary.data = post.summary
    form.content.data = post.content
    form.skill_1.data = post.skill_1
    form.skill_2.data = post.skill_2
    form.skill_3.data = post.skill_3
    form.skill_4.data = post.skill_4
    form.skill_5.data = post.skill_5
    return render_template('edit_entry.html', title='Update Entry', post=post, form=form, legend='Update the current entry')
  
  
@app.route("/champions/<int:champion_id>/delete", methods=['POST'])
@login_required
def delete(champion_id):
  post = Champion.query.get_or_404(champion_id)
  if post.author != current_user:
    abort(403)
  db.session.delete(post)
  db.session.commit()
  flash('Your entry has been deleted!', 'success')
  return redirect(url_for('championslist'))


@app.route("/champions/<int:champion_id>/change", methods=['GET', 'POST'])
def change_portait(champion_id):
  post = Champion.query.get_or_404(champion_id)
  form = UpdatePortait()
  if form.validate_on_submit():
    post.portait = form.portait.data
    db.session.commit()
    flash('The Portait has been updated!', 'success')
    return redirect(url_for('full_article', champion_id=post.id))
  elif request.method == 'GET':
    form.portait.data = post.portait
    return render_template('change_portait.html', title='Portait', post=post, form=form, legend='Change the current Portait')


@app.route("/upload", methods=['GET', 'POST'])
@login_required
def upload_picture():
  posts = Champion.query.all()
  form = PicturePost()
  pics = Pictures.query.order_by(Pictures.champion_id)
  if form.validate_on_submit(): 
    flash('The Picture has been uploaded!', 'success')
    post = Pictures(img_file=form.img_file.data,
                    champion_id=form.champion_id.data, champion_name=form.champion_name.data)
    db.session.add(post)
    db.session.commit()
    return redirect(url_for('gallery'))
  return render_template('upload_picture.html', title='Uploading', form=form, posts=posts, pics=pics)


@app.route("/gallery/<int:picture_id>", methods=['GET', 'POST'])
def full_picture(picture_id):
  pics = Pictures.query.get_or_404(picture_id)
  return render_template('full_picture.html', title=pics.champion_name, pics=pics)

@app.route("/gallery/<int:picture_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_picture(picture_id):
  pics = Pictures.query.get_or_404(picture_id)
  db.session.delete(pics)
  db.session.commit()
  flash('The picture has been deleted!', 'success')
  return redirect(url_for('gallery'))


@app.route("/gallery", methods=['GET', 'POST'])
def gallery():
  pics = Pictures.query.order_by(Pictures.champion_id) 
  return render_template('gallery.html', title='Gallery', pics=pics)


def send_reset_email(user):
  token = user.get_reset_token()
  msg = Message('Password Reset Request',
                sender='noreply@demo.com',
                recipients=[user.email])
  msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
  
If you did not make request, just ignore this email and no changes will be made.
'''
  mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
  if current_user.is_authenticated:
    return redirect(url_for('home'))
  form = RequestResetForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    send_reset_email(user)
    flash('An email has been sent to reset your password.', 'info')
    return redirect(url_for('login'))
  return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
  if current_user.is_authenticated:
    return redirect(url_for('home'))
  user = User.verify_reset_token(token)
  if user is None:
    flash('That is an expired or invalid token', 'warning')
    return redirect(url_for('reset_request'))
  form = ResetPasswordForm()
  if form.validate_on_submit():
    hashed_password = bcrypt.generate_password_hash(
        form.password.data).decode('utf-8')
    user.password = hashed_password
    db.session.commit()
    flash(f'Password has been updated! You are now able to log in.', 'success')
    return redirect(url_for('login'))
  return render_template('reset_token.html', title='Reset Password', form=form)


