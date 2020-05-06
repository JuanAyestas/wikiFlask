from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from palawiki.models import User

class RegistrationForm(FlaskForm):
  username = StringField('Username',
                          validators=[DataRequired(), Length(min=2, max=25)])
  email = StringField('Email',
                          validators=[DataRequired(), Email()])
  password = PasswordField('Password',
                          validators=[DataRequired()])
  confirm_password = PasswordField('Confirm Password',
                          validators=[DataRequired(), EqualTo('password')])
  submit = SubmitField('Sign Up')
  
  def validate_username(self, username):
    user = User.query.filter_by(username=username.data).first()
    if user:
      raise ValidationError(
          'That username is taken. Please use a different one.')

  def validate_email(self, email):
    user = User.query.filter_by(email=email.data).first()
    if user:
      raise ValidationError(
          'That email is taken. Please use a different one.')


class LoginForm(FlaskForm):
  email = StringField('Email',
                      validators=[DataRequired(), Email()])
  password = PasswordField('Password',
                      validators=[DataRequired()])
  remember = BooleanField('Remember Me')
  submit = SubmitField('Login')
  

class UpdateAccountForm(FlaskForm):
  username = StringField('Username',
                         validators=[DataRequired(), Length(min=2, max=25)])
  email = StringField('Email',
                      validators=[DataRequired(), Email()])
  picture_link = StringField('Enter the URL for the new picture', validators=[Length(min=10, max=500)])
  submit = SubmitField('Update info')

  def validate_username(self, username):
    if username.data != current_user.username:
      user = User.query.filter_by(username=username.data).first()
      if user :
        raise ValidationError(
            'That username is taken. Please use a different one.')

  def validate_email(self, email):
    if email.data != current_user.email:
      user = User.query.filter_by(email=email.data).first()
      if user:
        raise ValidationError(
            'That email is taken. Please use a different one.')


class ChampionPost(FlaskForm):
  name = StringField('Name', validators=[DataRequired()])
  title = StringField('Title', validators=[DataRequired()])
  role = StringField('Role', validators=[DataRequired()])
  hp = StringField('HP Stats', validators=[DataRequired()])
  speed = StringField('Movement Speed', validators=[DataRequired()])
  summary = TextAreaField('Info', validators=[DataRequired()])
  content = TextAreaField('Lore', validators=[DataRequired()])
  skill_1 = TextAreaField('Primary Fire', validators=[DataRequired()])
  skill_2 = TextAreaField('Secondary Fire', validators=[DataRequired()])
  skill_3 = TextAreaField('First Ability', validators=[DataRequired()])
  skill_4 = TextAreaField('Second Ability', validators=[DataRequired()])
  skill_5 = TextAreaField('Ultimate', validators=[DataRequired()])
  portait = StringField('URL for the champion portait',
                        validators=[DataRequired()])
  submit = SubmitField('Submit')


class UpdateChampion(FlaskForm):
  name = StringField('Name', validators=[DataRequired()])
  title = StringField('Title', validators=[DataRequired()])
  role = StringField('Role', validators=[DataRequired()])
  hp = StringField('HP Stats', validators=[DataRequired()])
  speed = StringField('Movement Speed', validators=[DataRequired()])
  summary = TextAreaField('Info', validators=[DataRequired()])
  content = TextAreaField('Lore', validators=[DataRequired()])
  skill_1 = TextAreaField('Primary Fire', validators=[DataRequired()])
  skill_2 = TextAreaField('Secondary Fire', validators=[DataRequired()])
  skill_3 = TextAreaField('First Ability', validators=[DataRequired()])
  skill_4 = TextAreaField('Second Ability', validators=[DataRequired()])
  skill_5 = TextAreaField('Ultimate', validators=[DataRequired()])
  submit = SubmitField('Save Changes')


class UpdatePortait(FlaskForm):
  portait = StringField('URL for the champion portait',
                        validators=[DataRequired(), Length(min=2, max=500)])
  submit = SubmitField('Save Changes')


class PicturePost(FlaskForm):
  img_file = StringField('Url for the champion picture', validators=[DataRequired()])
  champion_id = StringField('For which champion do you wanna upload it?', validators=[DataRequired()])
  champion_name = StringField('Select its title to confirm', validators=[DataRequired()])
  submit = SubmitField('Upload')


class RequestResetForm(FlaskForm):
  email = StringField('Email',
                      validators=[DataRequired(), Email()])
  submit = SubmitField('Request Password Reset')

  def validate_email(self, email):
      user = User.query.filter_by(email=email.data).first()
      if user is None:
        raise ValidationError(
            'There is not an accout with that email. Please register first.')
        

class ResetPasswordForm(FlaskForm):
  password = PasswordField('Password',
                           validators=[DataRequired()])
  confirm_password = PasswordField('Confirm Password',
                                   validators=[DataRequired(), EqualTo('password')])
  submit = SubmitField('Reset Password')
