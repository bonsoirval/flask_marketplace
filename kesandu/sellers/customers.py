from kesandu.sellers import bp

@bp.route('/catalog/categories/add_category')
def add_category():
    return 'Add categories'

@bp.route('/customers/view_customers')
def view_customers():
    return "View customers"

@bp.route('/customers/view_customer_group')
def view_customer_group():
    pass

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