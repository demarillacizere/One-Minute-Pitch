from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,SelectField
from wtforms.validators import Required

class PitchForm(FlaskForm):

 title = StringField('Pitch title',validators=[Required()])
 content = TextAreaField('Pitch', validators=[Required()])
 category = SelectField('Category', choices=[('Advertisement','Advertisement Pitch'),('Project','Project Pitch'),('General','General Pitch'),('Sale','Sale Pitch')], validators=[Required()])
 submit = SubmitField('Submit')
 

class CommentForm(FlaskForm):

 comment = TextAreaField('Movie review', validators=[Required()])

 submit = SubmitField('Submit')

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')