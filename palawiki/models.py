from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer 
from flask_login import UserMixin
from flask import current_app
from palawiki import db, login_manager

@login_manager.user_loader
def load_user(user_id):
  return User.query.get_or_404(int(user_id))

class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(25), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  image_file = db.Column(db.String(300), nullable=False,
                         default="static/profile_pics/default.jpg")
  password = db.Column(db.String(60), nullable=False)
  # relationship with champion
  champion = db.relationship('Champion', backref='author', lazy=True)
  
  def get_reset_token(self, expires_sec=1800):
    s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
    return s.dumps({'user_id':self.id}).decode('utf-8')
  
  
  @staticmethod
  def verify_reset_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
      user_id = s.loads(token)['user_id']
    except:
      return None
    return User.query.get(user_id)
    

  def __repr__(self):
    return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Champion(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False)
  title = db.Column(db.String(50), nullable=False)
  role = db.Column(db.String(20), nullable=False)
  hp = db.Column(db.Text, nullable=False)
  speed = db.Column(db.Text, nullable=False)
  summary = db.Column(db.Text, nullable=False)
  content = db.Column(db.Text, nullable=False)
  skill_1 = db.Column(db.Text, nullable=False)
  skill_2 = db.Column(db.Text, nullable=False)
  skill_3 = db.Column(db.Text, nullable=False)
  skill_4 = db.Column(db.Text, nullable=False)
  skill_5 = db.Column(db.Text, nullable=False)
  date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  portait = db.Column(db.String(500), nullable=False)
  # relationship with User
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  # relationship with Pictures
  champion_id = db.relationship('Pictures', backref='champion', lazy=True)

  def __repr__(self):
    return f"Champion('{self.name}', '{self.date_posted})"


class Pictures(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  img_file = db.Column(db.String(500), nullable=False)
  # relationship with champion
  champion_id = db.Column(
      db.Integer, db.ForeignKey('champion.id'), nullable=False)
  champion_name = db.Column(db.Text, nullable=False)

  def __repr__(self):
    return f"Pictures('{self.img_file}')"
