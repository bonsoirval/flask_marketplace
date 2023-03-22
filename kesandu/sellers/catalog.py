import pandas as pd
from kesandu import db
from flask_login import current_user
from kesandu.sellers import bp
from flask import render_template, request
from flask_login import login_required
from sqlalchemy import text, select, or_, and_, not_, join 
from kesandu.frontend.models import Product, ProductDescription
from kesandu.sellers.forms import AddProductForm
# from kesandu.sellers.models import Categories


@bp.route('/sellers/catalog/view_categories', methods=['GET', 'POST'])
@login_required
def view_categories():
    parents = text("SELECT c.id, c.parent_id, c.sort_order, cd.id, \
        cd.name \
        FROM category AS c \
                JOIN category_description AS cd \
                    ON cd.category_id = c.id \
                        GROUP BY cd.name \
                            ORDER BY cd.id")
    
    children = text("SELECT c.id, c.image, c.parent_id,c.sort_order, cd.id AS description_id, cd.name FROM category AS c \
        JOIN category_description AS cd ON c.id = cd.category_id")
    parents_df = pd.read_sql(con = db.engine , sql = parents)
    children_df = pd.read_sql(con = db.engine, sql = children)
    
    parents = [{'parent_id': i[0:][0],'sort_order':i[0:][2], 'parent_name':i[0:][4] } for i in parents_df[parents_df['parent_id'] == 0].values]
    children_df =[{'id':i[0:][0], 'image':i[0:][1], 'parent_id':i[0:][2],'sort_order':i[0:][3], 'description_id':i[0:][4], 'child_name':i[0:][5]} for i in children_df[children_df['parent_id'] != 0].values] # [{'child_id': i[0:]} for i in children_df] #[children_df['parent_id' != 0]].values]
    data = {
        'title': "Sellers Categories",
        'parents_df' : parents_df,
        'parents' : parents,
        'children': children_df
    }
    
    # return render_template('dummy/dummy.html', data = data)
    return render_template('sellers/catalog/category.html', data=data)

@bp.route('/sellers/catalog/edit_category/cat_id/')
@login_required
def edit_category(cat_id):
    return "Edit Category : {cat_id}".format(cat_id)

@bp.route('/sellers/catalog/edit_product/<product_id>')
@login_required
def s_edit_product(product_id):
    return product_id

@bp.route('/sellers/catalog/add_product', methods=['GET', 'POST'])
@login_required
def s_add_product():
    form = AddProductForm(request.form)
    from kesandu.sellers.forms import FakeLoginForm
    
    # form = FakeLoginForm()
    
    if form.validate_on_submit(): 
        """NOTE: 
        shipping : {form.shipping.data} <br/> comes immediately after stock_status_id
        weight_class_id : {form.weight_class_id.data} <br/>  just below weight
        weight : {form.weight.data} <br/>  just below length_class_id
        sort_order : {form.sort_order.data} just below status <br/> 
        """ 
        return f"Product Name : {form.product_name.data} <br/> \
            Product Description : {form.product_description.data} <br/> \
            Product Meta Tag : {form.meta_tag_title.data} <br/> \
            Product meta tag description : {form.meta_tag_description.data} <br/> \
            Product meta tag keywords : {form.meta_tag_keywords.data} <br/>\
            Product tags : {form.product_tags.data} <br/>\
            model : {form.model.data} <br/> \
            sku : {form.sku.data} <br/>\
            upc : {form.upc.data} <br/> \
            ean : {form.ean.data} <br/> \
            jan : {form.jan.data} <br/> \
            isbn : {form.isbn.data} <br/>\
            mpn : {form.mpn.data} <br/> \
            location : {form.location.data} <br/> \
            price : {form.price.data} <br/>\
            tax_class : {form.tax_class.data} <br/> \
            quantity : {form.quantity.data} <br/> \
            min_quantity : {form.min_quantity.data} <br/>\
            subtract_stock : {form.subtract_stock.data} <br/> \
            stock_status_id : {form.stock_status_id.data} <br/> \
            shipping : {form.shipping.data} <br/> \
            date_available : {form.date_available.data} <br/> \
            length : {form.length.data} <br/> \
            width : {form.width.data} <br/> \
            height : {form.height.data} <br/>  \
            # length_class_id : {form.length_class_id.data} <br/> \
            weight : {form.weight.data} <br/> \
            weight_class_id : {form.weight_class_id.data} <br/>\
            status : {form.status.data} <br/> \
            sort_order : {form.sort_order.data} <br/>\
            manufacturer : {form.manufacturer.data} <br/>  \
            category : {form.category.data} <br/>" #\
            # filters : {form.filters.data} <br/>\
            # stores : {form.stores.data} <br/>\
            # downloads : {form.downloads.data} <br/>\
            # related_products : {form.related_prdoucts.data} <br/>\
            # image : {form.images.data} <br/>\
    
    # if form.validate_on_submit():
    #     return'Not valid product'
    
    # if request.method == 'POST' and form.validate():
    #     return 'validated'
        
    data = {
        'title': 'Add Product',
        'form': form
    }
    # return render_template('dummy/dummy.html', data=data, form=form)
    return render_template('sellers/catalog/add_product.html', data=data)

@bp.route('/sellers/catalog/copy_product', methods=['GET', 'POST'])
@login_required
def s_copy_product():
    return 'copy product'

@bp.route('/sellers/catalog/delete_product', methods=['GET', 'POST'])
@login_required
def s_delete_product():
    return 'delete product'

@bp.route('/catalog/view_products')
@login_required
def view_products():
    products = (
        Product.query
            .join(ProductDescription)
            .with_entities(ProductDescription.name, 
                           Product.model,
                           Product.price,
                           Product.status,
                           Product.quantity)
            .where(Product.id,ProductDescription.product_id)
            .filter(Product.seller_id == current_user.id)
            .all()
    )
    data = {
        'title': "Seller's Product",
        'products': products
    }
    return render_template('sellers/catalog/products.html', data=data)

@bp.route('/catalog/view_recurring_profiles')
def view_recurring_profiles():
    return render_template('sellers/catalog/recurring_profiles.html')

def filters():
    pass 

def attributes():
    pass 

def options():
    pass

def manufacturers():
    return 'manufacturers'

def downloads():
    return "downloads"

def reviews():
    return 'reviews'

def information():
    return 'information'
