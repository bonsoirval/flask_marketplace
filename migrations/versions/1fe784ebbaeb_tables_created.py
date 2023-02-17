"""Tables created

Revision ID: 1fe784ebbaeb
Revises: 
Create Date: 2023-02-17 10:54:50.004527

"""
from alembic import op
import sqlalchemy as sa
import flask_authorize


# revision identifiers, used by Alembic.
revision = '1fe784ebbaeb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin',
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
    op.create_table('groups',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('restrictions', flask_authorize.mixins.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uid', sa.Integer(), nullable=True),
    sa.Column('ofname', sa.Text(), nullable=False),
    sa.Column('pid', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('oplace', sa.Text(), nullable=False),
    sa.Column('mobile', sa.String(length=15), nullable=False),
    sa.Column('dstatus', sa.String(length=10), nullable=False),
    sa.Column('odate', sa.DateTime(), nullable=False),
    sa.Column('ddate', sa.Date(), nullable=False),
    sa.PrimaryKeyConstraint('id')
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
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('allowances', flask_authorize.mixins.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.Column('mobile', sa.String(length=14), nullable=False),
    sa.Column('reg_time', sa.DateTime(), nullable=True),
    sa.Column('activation', sa.String(length=3), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
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
    op.drop_table('users')
    op.drop_table('roles')
    op.drop_table('products')
    op.drop_table('product_views')
    op.drop_table('product_levels')
    op.drop_table('orders')
    op.drop_table('groups')
    op.drop_table('admin')
    # ### end Alembic commands ###
