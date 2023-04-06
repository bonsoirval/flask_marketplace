import pandas as pd
from kesandu import db
from flask_login import current_user
from kesandu.sellers import bp
from flask import render_template, request, current_app, abort, redirect, url_for, jsonify
from flask_login import login_required
from sqlalchemy import text, select, or_, and_, not_, join 
from kesandu.frontend.models import Product, ProductDescription
from kesandu.sellers.forms import AddProductForm, TestFileUpload
from werkzeug.utils import secure_filename
import imghdr
import os
from datetime import datetime

@bp.route('/sellerrs/catalog/get_manufacturer')
def s_get_manufacturer():
    return jsonify({
        '1': 'okechukwu',
        '2': 'njoku'
    })
def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.'+(format if format != 'jpeg' else 'jpg')

def upload_file(success_page="s_add_product"):
    uploaded_file = request.files['file']
    uploaded_file.filename = os.path.splitext(uploaded_file.filename)[0] + "_seller_" \
        + str(current_user.id) + os.path.splitext(uploaded_file.filename)[1]
    
    filename = secure_filename(uploaded_file.filename).split('/')[-1]
    if uploaded_file.filename != "":
        file_ext = os.path.splitext(uploaded_file.filename)[1]
        if file_ext not in current_app.config['UPLOAD_EXTENSIONS'] or file_ext != validate_image(uploaded_file.stream):
            abort(400)
        saved_file = os.path.join(current_app.config['SELLERS_PRODUCT'], filename)
        uploaded_file.save(saved_file) 
        return saved_file
    return f"File Not Saved", 400 # redirect(url_for(success_page))

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
# @login_required
def s_add_product():
    form = AddProductForm(request.form)
   
    # upload_file(page='sellerssuccess_.s_add_product')
   
    
    if form.validate_on_submit(): 
        # """NOTE: 
        # shipping : {form.shipping.data} <br/> comes immediately after stock_status_id
        # weight_class_id : {form.weight_class_id.data} <br/>  just below weight
        # weight : {form.weight.data} <br/>  just below length_class_id
        # sort_order : {form.sort_order.data} just below status <br/> 
        # """ 
        # """ Create Product and ProductDescription objects"""
        # product and product_description objects 

        product = Product.query \
            .filter_by(model = form.model.data, seller_id = current_user.id) \
                .join(ProductDescription) \
                    .where(Product.id, ProductDescription.product_id) \
                        .first()
        
        
        # if product already exists, from same , do not upload it again
        if product: # and prod_description:
            return redirect(url_for('sellers.s_add_product')) # f'the product exists already {product}'
        else:
            """ 
            Put sku, ean and other parameters into consideration."""
            # Create database object
            prod_params = {
                'seller_id' : current_user.id,
                'model' : form.model.data,
                'sku' : form.sku.data,
                'upc' : form.upc.data,
                'ean' : form.ean.data,
                'jan' : form.jan.data,
                'isbn' : form.isbn.data,
                'mpn' : form.mpn.data, 
                'location' : form.location.data,
                'price' : form.price.data,
                'tax_class_id' : form.tax_class.data,
                'quantity' : form.quantity.data,
                'minimum' : form.minimum.data,
                'subtract' : form.subtract.data,
                'stock_status_id' : form.stock_status_id.data,
                'shipping' : form.shipping.data,
                'date_available' : form.date_available.data,
                'length' : form.length.data,
                'width' : form.width.data,
                'height' : form.height.data,
                # 'length_class_id' : form.length_class_id.data,
                'weight' : form.weight.data,
                'weight_class_id' : form.weight_class_id.data,
                'status' : form.status.data,
                'manufacturer_id' : form.manufacturer_id.data,
                # 'category' : form.category.data,
                # 'filters' : form.filters.data,
                # 'stores' : form.stores.data,
                # 'downloads' : form.downloads.data,
                # 'related' : form.related.data,
                'image' : upload_file(success_page='sellerssuccess_.s_add_product'),
                'date_added' : datetime.utcnow(),
                'date_modified' : datetime.utcnow()
            }
            product = Product(**prod_params)
            db.session.add(product)
            db.session.flush()
            # db.session.refresh(product)
           
            
            prod_desc_params = {
                'language_id': 1,
                'product_id' : product.id,
                'name' : form.product_name.data, 
                'description' : form.description.data,
                'tag' : form.tags.data,
                'meta_title' : form.meta_title.data,
                'meta_description' : form.meta_description.data,
                'meta_keyword' : form.meta_keywords.data
            }
           
            product_description = ProductDescription(**prod_desc_params)
            db.session.add(product_description)
            db.session.commit()            
            return redirect(url_for('sellers.s_add_product'))
         
    data = {
        'title': 'Add Product',
        'form': form
    }

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
