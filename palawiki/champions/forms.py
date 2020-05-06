from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


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

