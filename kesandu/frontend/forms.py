from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SelectField
from kesandu import mysql



class OrderForm(Form):  # Create Order Form
    name = StringField('', [validators.length(min=1), validators.DataRequired()],
                       render_kw={'autofocus': True, 'placeholder': 'Full Name'})
    mobile_num = StringField('', [validators.length(min=1), validators.DataRequired()],
                             render_kw={'autofocus': True, 'placeholder': 'Mobile'})
    quantity = SelectField('', [validators.DataRequired()],
                           choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')])
    order_place = StringField('', [validators.length(min=1), validators.DataRequired()],
                              render_kw={'placeholder': 'Order Place'})


# from flask import request
# from flask_wtf import FlaskForm
# from wtforms import StringField, SubmitField, TextAreaField
# from wtforms.validators import ValidationError, DataRequired, Length
# from flask_babel import _, lazy_gettext as _l
# from kesandu.frontend.models import User


# class EditProfileForm(FlaskForm):
#     username = StringField(_l('Username'), validators=[DataRequired()])
#     about_me = TextAreaField(_l('About me'),
#                              validators=[Length(min=0, max=140)])
#     submit = SubmitField(_l('Submit'))

#     def __init__(self, original_username, *args, **kwargs):
#         super(EditProfileForm, self).__init__(*args, **kwargs)
#         self.original_username = original_username

#     def validate_username(self, username):
#         if username.data != self.original_username:
#             user = User.query.filter_by(username=self.username.data).first()
#             if user is not None:
#                 raise ValidationError(_('Please use a different username.'))


# class EmptyForm(FlaskForm):
#     submit = SubmitField('Submit')


# class PostForm(FlaskForm):
#     post = TextAreaField(_l('Say something'), validators=[DataRequired()])
#     submit = SubmitField(_l('Submit'))

