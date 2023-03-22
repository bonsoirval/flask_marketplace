from kesandu.admin import bp 

@bp.route('/admin')
def a_home():
    return 'admin index'
