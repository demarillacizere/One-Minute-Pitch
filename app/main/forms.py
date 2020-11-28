from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,SelectField
from wtforms.validators import Required

class PitchForm(FlaskForm):

 title = StringField('Pitch title',validators=[Required()])
 content = TextAreaField('Pitch', validators=[Required()])
 category = SelectField('Category', choices=[('Interview','Interview'),('Advertisement','Advertisement'),('Project','Project'),('General','General'),('Pickuplines','Pickuplines')], validators=[Required()])
 submit = SubmitField('Submit')
 

class CommentForm(FlaskForm):

 comment = TextAreaField('Comment', validators=[Required()])

 submit = SubmitField('Submit')

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')