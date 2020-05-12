from flask import (render_template, redirect, url_for,
                    flash, request, abort, Blueprint)
from flask_login import current_user, login_required
from palawiki import db
from palawiki.models import Champion, Pictures
from palawiki.champions.forms import (ChampionPost, PicturePost, UpdateChampion,
                            UpdatePortait)

champions = Blueprint('champions', __name__)


@champions.route("/create", methods=['POST', 'GET'])
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
    return redirect(url_for('main.championslist'))
  return render_template('new_entry.html', title='New Entry', form=form, legend='Create a new entry')


@champions.route("/champions/<int:champion_id>/edit", methods=['GET', 'POST'])
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
    return redirect(url_for('main.full_article', champion_id=post.id))
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


@champions.route("/champions/<int:champion_id>/delete", methods=['POST'])
@login_required
def delete(champion_id):
  post = Champion.query.get_or_404(champion_id)
  if post.author != current_user:
    abort(403)
  db.session.delete(post)
  db.session.commit()
  flash('Your entry has been deleted!', 'success')
  return redirect(url_for('main.championslist'))


@champions.route("/champions/<int:champion_id>/change", methods=['GET', 'POST'])
def change_portait(champion_id):
  post = Champion.query.get_or_404(champion_id)
  form = UpdatePortait()
  if form.validate_on_submit():
    post.portait = form.portait.data
    db.session.commit()
    flash('The Portait has been updated!', 'success')
    return redirect(url_for('main.full_article', champion_id=post.id))
  elif request.method == 'GET':
    form.portait.data = post.portait
    return render_template('change_portait.html', title='Portait', post=post, form=form, legend='Change the current Portait')


@champions.route("/upload", methods=['GET', 'POST'])
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
    return redirect(url_for('main.gallery'))
  return render_template('upload_picture.html', title='Uploading', form=form, posts=posts, pics=pics, legend="Upload a new Picture")


@champions.route("/gallery/<int:picture_id>", methods=['GET', 'POST'])
def full_picture(picture_id):
  pics = Pictures.query.get_or_404(picture_id)
  return render_template('full_picture.html', title=pics.champion_name, pics=pics)


@champions.route("/gallery/<int:picture_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_picture(picture_id):
  pics = Pictures.query.get_or_404(picture_id)
  db.session.delete(pics)
  db.session.commit()
  flash('The picture has been deleted!', 'success')
  return redirect(url_for('main.gallery'))
