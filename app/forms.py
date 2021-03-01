from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, SubmitField

from wtforms.validators import DataRequired, Required

class InputDataForm(FlaskForm):
    minimal_latitude = StringField('Minimal latitude', validators=[DataRequired()], id='min_lat')
    maximal_latitude = StringField('Maximal latitude', validators=[DataRequired()], id='max_lat')
    minimal_longitude = StringField('Minimal longitude', validators=[DataRequired()], id='min_lon')
    maximal_longitude = StringField('Maximal longitude', validators=[DataRequired()], id='max_lon')
    date_from = DateTimeField(validators=[Required()], id='date_from')
    date_to = DateTimeField(validators=[Required()], id='date_to')
    current_date = DateTimeField(validators=[Required()], id='current_date')
    send_data = SubmitField('Применить', id='send_id')
    quality = StringField('Quality', validators=[DataRequired()], id='quality')