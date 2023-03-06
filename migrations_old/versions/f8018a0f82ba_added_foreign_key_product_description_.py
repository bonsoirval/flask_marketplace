"""Added foreign key product_description.product_id ==> product.id 

Revision ID: f8018a0f82ba
Revises: f44497826182
Create Date: 2023-03-01 07:03:22.836277

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f8018a0f82ba'
down_revision = 'f44497826182'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('cart', 'id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True,
               autoincrement=True)
    op.alter_column('order_option', 'id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True,
               autoincrement=True)
    op.alter_column('order_product', 'id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.add_column('product_description', sa.Column('product_id', mysql.INTEGER(display_width=11), nullable=False))
    op.create_foreign_key(None, 'product_description', 'products', ['product_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'product_description', type_='foreignkey')
    op.drop_column('product_description', 'product_id')
    op.alter_column('order_product', 'id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column('order_option', 'id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False,
               autoincrement=True)
    op.alter_column('cart', 'id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False,
               autoincrement=True)
    # ### end Alembic commands ###
