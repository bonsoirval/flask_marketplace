from flask_wtf import FlaskForm
from wtforms import FileField, DateField, RadioField, StringField, PasswordField, BooleanField, SubmitField, TextField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_wtf.file import FileField, FileAllowed, FileRequired
from kesandu.sellers.models import Seller


class TestFileUpload(FlaskForm):
    file = FileField('file')
    submit = SubmitField('submit')

class FakeLoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
    
class AddProductForm(FlaskForm):
    product_name = StringField('Product Name', validators=[DataRequired()])
    product_description = TextField('Product Description')
    meta_tag_title = StringField('Meta Tag Title', validators=[DataRequired()])
    meta_tag_description = TextField('Meta Tag Description')
    meta_tag_keywords = TextField('Meta Tag Keywords')
    product_tags = StringField('Product Tags')
    model = StringField('Model', validators = [DataRequired()])
    sku = StringField('SKU')
    upc = StringField('UPC')
    ean = StringField('EAN')
    jan = StringField('JAN')
    isbn = StringField('ISBN')
    mpn = StringField('MPN')
    location = StringField('Location')
    price = StringField('Price')
    tax_class = SelectField('Tax Class', choices=[('0','Make Select'), ('9', 'Taxable Goods'), ('10', 'Downloadable Products')])
    quantity = StringField('Quantity')
    min_quantity = StringField('Minimum Quantity') # , min_entries=1)
    subtract_stock = SelectField('Subtract Stock', choices=[('1', 'Yes'), ('0', 'No')])
    stock_status_id = SelectField('Out Of Stock Status', choices=[('6', '2-3 Days'), ('7', 'In Stock'), ('5', 'Out Of Stock'), ('8','Pre-Order')])
    shipping = RadioField('Requires Shipping', choices=[('1', 'Yes'), ('0', 'No')], default=1, coerce=int, validators=[DataRequired()])
    date_available = DateField('Available Data', format='%Y-%m-%d' )
    length = StringField('Length')
    width = StringField('Width')
    height = StringField('Height')
    length_class_id = SelectField('Length Class',choices=[('1', 'Centimeters'),('2', 'Milimeters'),('3', 'Inches')]) 
    weight = StringField('Weight')
    weight_class_id = SelectField('Weight Class',choices=[('1', 'Kilograms'), ('2', 'Gram'), ('5', 'Pound'), ('6', 'Ounce')])
    status = SelectField('Status',choices=[('1', 'Enabled'), ('2', 'Disabled')])
    sort_order = StringField('Sort Order')
    manufacturer = StringField('Manufacturer [Ajax filled]')
    manufacturer_id = StringField('Manufacturer_id')
    category = StringField('Category [Ajax filled]')
    filters = StringField('Filters (deactivated)')
    stores = StringField('Store [Ajax filled]') # , value='default')
    downloads = StringField('Download')
    related = StringField('Related Products [ajax filled]')
    # image = FileField("photo", validators=[FileRequired()]) #, FileAllowed(['jpg','jpeg','png'], 'Images Only Allowed')])
    
    submit = SubmitField('Add Product')                        
            
    
    
class SellersLoginForm(FlaskForm):
    username = StringField('Seller Username', validators = [DataRequired()])
    password = PasswordField("Seller Password", validators = [DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

# class SellerLoginForm(FlaskForm):
#     username = StringField("Username", validators=[DataRequired()])
#     password = PasswordField("Password", validators=[DataRequired()])
#     remember_me = BooleanField("Remember Me")
#     submit = SubmitField("Submit")
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        seller = Seller.query.filter_by(username=username.data).first()
        if seller is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        seller = Seller.query.filter_by(email=email.data).first()
        if seller is not None:
            raise ValidationError('Please use a different email address.')
