"""user table returned to original form

Revision ID: 59c0113a8e1c
Revises: a2fdbfa2ff1e
Create Date: 2023-02-17 12:41:24.197431

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '59c0113a8e1c'
down_revision = 'a2fdbfa2ff1e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.add_column('users', sa.Column('email', sa.String(length=50), nullable=False))
    op.add_column('users', sa.Column('username', sa.String(length=50), nullable=False))
    op.add_column('users', sa.Column('password_hash', sa.String(length=128), nullable=False))
    op.add_column('users', sa.Column('mobile', sa.String(length=14), nullable=False))
    op.add_column('users', sa.Column('reg_time', sa.DateTime(), nullable=True))
    op.add_column('users', sa.Column('online', sa.String(length=1), nullable=False))
    op.add_column('users', sa.Column('activation', sa.String(length=3), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'activation')
    op.drop_column('users', 'online')
    op.drop_column('users', 'reg_time')
    op.drop_column('users', 'mobile')
    op.drop_column('users', 'password_hash')
    op.drop_column('users', 'username')
    op.drop_column('users', 'email')
    op.create_table('user',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('name', mysql.VARCHAR(length=50), nullable=False),
    sa.Column('email', mysql.VARCHAR(length=50), nullable=False),
    sa.Column('username', mysql.VARCHAR(length=50), nullable=False),
    sa.Column('password_hash', mysql.VARCHAR(length=128), nullable=False),
    sa.Column('mobile', mysql.VARCHAR(length=14), nullable=False),
    sa.Column('reg_time', mysql.DATETIME(), nullable=True),
    sa.Column('online', mysql.VARCHAR(length=1), nullable=False),
    sa.Column('activation', mysql.VARCHAR(length=3), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='latin1',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###
