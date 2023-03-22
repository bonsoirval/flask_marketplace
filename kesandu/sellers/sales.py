from kesandu.sellers import bp

@bp.route('/sales/view_orders')
def view_orders():
    return "view orders"

@bp.route('/sales/add_order')
def add_order():
    return 'add order'

@bp.route('/sales/edit_order')
def edit_order():
    return 'edit order'

@bp.route('sales/delete_order')
def delete_order():
    return 'delete order'

@bp.route('/sales/view_recurring_profile')
def view_recurring_profile():
    return 'view recurring profile'

@bp.route('/sales/view_returns')
def view_returns():
    return 'view return'