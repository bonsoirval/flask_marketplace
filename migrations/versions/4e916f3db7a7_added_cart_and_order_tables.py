"""Added cart and order tables

Revision ID: 4e916f3db7a7
Revises: 
Create Date: 2023-02-20 02:41:26.413764

"""
from alembic import op
import sqlalchemy as sa
import flask_authorize


# revision identifiers, used by Alembic.
revision = '4e916f3db7a7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('groups',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('restrictions', flask_authorize.mixins.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('product_levels',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('v_shape', sa.String(length=10), nullable=False),
    sa.Column('polo', sa.String(length=10), nullable=False),
    sa.Column('clean_text', sa.String(length=10), nullable=False),
    sa.Column('design', sa.String(length=10), nullable=False),
    sa.Column('chain', sa.String(length=10), nullable=False),
    sa.Column('leather', sa.String(length=10), nullable=False),
    sa.Column('hook', sa.String(length=10), nullable=False),
    sa.Column('color', sa.String(length=10), nullable=False),
    sa.Column('formal', sa.String(length=10), nullable=False),
    sa.Column('converse', sa.String(length=10), nullable=False),
    sa.Column('loafer', sa.String(length=10), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('product_views',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('allowances', flask_authorize.mixins.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('sellers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('firstName', sa.String(length=125), nullable=False),
    sa.Column('lastName', sa.String(length=125), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('mobile', sa.String(length=25), nullable=False),
    sa.Column('address', sa.Text(), nullable=False),
    sa.Column('password_hash', sa.String(length=100), nullable=False),
    sa.Column('type', sa.String(length=20), nullable=False),
    sa.Column('confirmCode', sa.String(length=10), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.Column('mobile', sa.String(length=14), nullable=False),
    sa.Column('reg_time', sa.DateTime(), nullable=True),
    sa.Column('online', sa.String(length=1), nullable=False),
    sa.Column('activation', sa.String(length=3), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cart',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('api_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('session_id', sa.String(length=32), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('recurring_id', sa.Integer(), nullable=False),
    sa.Column('option', sa.Text(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('date_added', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('invoice_no', sa.Integer(), nullable=False),
    sa.Column('invoice_prefix', sa.String(length=26), nullable=False),
    sa.Column('seller_id', sa.Integer(), nullable=False),
    sa.Column('store_url', sa.String(length=255), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('customer_group_id', sa.Integer(), nullable=False),
    sa.Column('firstname', sa.String(length=32), nullable=False),
    sa.Column('lastname', sa.String(length=32), nullable=False),
    sa.Column('email', sa.String(length=96), nullable=False),
    sa.Column('telephone', sa.String(length=32), nullable=False),
    sa.Column('fax', sa.String(length=32), nullable=False),
    sa.Column('custom_field', sa.Text(), nullable=False),
    sa.Column('payment_firstname', sa.String(length=32), nullable=False),
    sa.Column('payment_lastname', sa.String(length=32), nullable=False),
    sa.Column('payment_company', sa.String(length=60), nullable=False),
    sa.Column('payment_address_1', sa.String(length=128), nullable=False),
    sa.Column('payment_address_2', sa.String(length=128), nullable=False),
    sa.Column('payment_city', sa.String(length=128), nullable=False),
    sa.Column('payment_postcode', sa.String(length=10), nullable=False),
    sa.Column('payment_country', sa.String(length=128), nullable=False),
    sa.Column('payment_country_id', sa.Integer(), nullable=False),
    sa.Column('payment_zone', sa.String(length=128), nullable=False),
    sa.Column('payment_zone_id', sa.Integer(), nullable=False),
    sa.Column('payment_address_format', sa.Text(), nullable=False),
    sa.Column('payment_custom_field', sa.Text(), nullable=False),
    sa.Column('payment_method', sa.String(length=128), nullable=False),
    sa.Column('payment_code', sa.String(length=128), nullable=False),
    sa.Column('shipping_firstname', sa.String(length=32), nullable=False),
    sa.Column('shipping_lastname', sa.String(length=32), nullable=False),
    sa.Column('shipping_company', sa.String(length=40), nullable=False),
    sa.Column('shipping_address_1', sa.String(length=128), nullable=False),
    sa.Column('shipping_address_2', sa.String(length=128), nullable=False),
    sa.Column('shipping_city', sa.String(length=128), nullable=False),
    sa.Column('shipping_postcode', sa.String(length=10), nullable=False),
    sa.Column('shipping_country', sa.String(length=128), nullable=False),
    sa.Column('shipping_country_id', sa.Integer(), nullable=False),
    sa.Column('shipping_zone', sa.String(length=128), nullable=False),
    sa.Column('shipping_zone_id', sa.Integer(), nullable=False),
    sa.Column('shipping_address_format', sa.Text(), nullable=False),
    sa.Column('shipping_custom_field', sa.Text(), nullable=False),
    sa.Column('shipping_method', sa.String(length=128), nullable=False),
    sa.Column('shipping_code', sa.String(length=128), nullable=False),
    sa.Column('comment', sa.Text(), nullable=False),
    sa.Column('total', sa.Float(precision=15, asdecimal=4), nullable=False),
    sa.Column('order_status_id', sa.Integer(), nullable=False),
    sa.Column('affiliate_id', sa.Integer(), nullable=False),
    sa.Column('commission', sa.Float(precision=15, asdecimal=4), nullable=False),
    sa.Column('marketing_id', sa.Integer(), nullable=False),
    sa.Column('tracking', sa.String(length=64), nullable=False),
    sa.Column('language_id', sa.Integer(), nullable=False),
    sa.Column('currency_id', sa.Integer(), nullable=False),
    sa.Column('currency_code', sa.String(length=3), nullable=False),
    sa.Column('currency_value', sa.Float(precision=15, asdecimal=8), nullable=False),
    sa.Column('ip', sa.String(length=40), nullable=False),
    sa.Column('forwarded_ip', sa.String(length=40), nullable=False),
    sa.Column('user_agent', sa.String(length=255), nullable=False),
    sa.Column('accept_language', sa.String(length=255), nullable=False),
    sa.Column('date_added', sa.DateTime(), nullable=False),
    sa.Column('date_modified', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_name', sa.String(length=100), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('available', sa.Integer(), nullable=False),
    sa.Column('category', sa.String(length=100), nullable=False),
    sa.Column('item', sa.String(length=100), nullable=False),
    sa.Column('product_code', sa.String(length=20), nullable=False),
    sa.Column('picture', sa.Text(), nullable=False),
    sa.Column('seller_id', sa.Integer(), nullable=True),
    sa.Column('keywords', sa.String(length=120), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['seller_id'], ['sellers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_group',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('group_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )
    op.create_table('user_role',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_role')
    op.drop_table('user_group')
    op.drop_table('products')
    op.drop_table('orders')
    op.drop_table('cart')
    op.drop_table('users')
    op.drop_table('sellers')
    op.drop_table('roles')
    op.drop_table('product_views')
    op.drop_table('product_levels')
    op.drop_table('groups')
    # ### end Alembic commands ###
