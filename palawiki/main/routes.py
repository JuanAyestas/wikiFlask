from flask import Blueprint, render_template, redirect, request
from palawiki.models import Champion, User, Pictures

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    return render_template('home.html', title='Home')


@main.route("/champions")
def championslist():
  page = request.args.get('page', 1, type=int)
  posts = Champion.query.order_by(
      Champion.name.asc()).paginate(page=page, per_page=3)
  return render_template('champion_list.html', title='Champions List', posts=posts)


@main.route("/champions/<int:champion_id>", methods=['GET', 'POST'])
def full_article(champion_id):
  post = Champion.query.get_or_404(champion_id)
  return render_template('full_article.html', title=post.name, post=post)


@main.route("/user/<string:username>")
def user_posts(username):
  page = request.args.get('page', 1, type=int)
  user = User.query.filter_by(username=username).first_or_404()
  posts = Champion.query.filter_by(author=user)\
      .order_by(Champion.name.asc())\
      .paginate(page=page, per_page=4)
  return render_template('user_posts.html', title='Champions List', posts=posts, user=user)


@main.route("/gallery", methods=['GET', 'POST'])
def gallery():
  pics = Pictures.query.order_by(Pictures.champion_id)
  return render_template('gallery.html', title='Gallery', pics=pics)
