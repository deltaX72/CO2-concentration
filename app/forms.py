from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, SubmitField

from wtforms.validators import DataRequired, Required

class InputDataForm(FlaskForm):
    minimal_latitude = StringField('Minimal latitude', validators=[DataRequired()], id='min_lat')
    maximal_latitude = StringField('Maximal latitude', validators=[DataRequired()], id='max_lat')
    minimal_longitude = StringField('Minimal longitude', validators=[DataRequired()], id='min_lon')
    maximal_longitude = StringField('Maximal longitude', validators=[DataRequired()], id='max_lon')
    date_from = DateTimeField(format='%d%m%y', validators=[Required()])
    date_to = DateTimeField(format='%d%m%y', validators=[Required()])
    send_data = SubmitField('Send', id='send_id')