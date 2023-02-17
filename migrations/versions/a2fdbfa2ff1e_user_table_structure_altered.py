"""user table structure altered

Revision ID: a2fdbfa2ff1e
Revises: de69443a578a
Create Date: 2023-02-17 12:35:25.214082

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a2fdbfa2ff1e'
down_revision = 'de69443a578a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
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
    op.drop_column('users', 'online')
    op.drop_column('users', 'mobile')
    op.drop_column('users', 'reg_time')
    op.drop_column('users', 'activation')
    op.drop_column('users', 'email')
    op.drop_column('users', 'password_hash')
    op.drop_column('users', 'username')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('username', mysql.VARCHAR(length=50), nullable=False))
    op.add_column('users', sa.Column('password_hash', mysql.VARCHAR(length=128), nullable=False))
    op.add_column('users', sa.Column('email', mysql.VARCHAR(length=50), nullable=False))
    op.add_column('users', sa.Column('activation', mysql.VARCHAR(length=3), nullable=False))
    op.add_column('users', sa.Column('reg_time', mysql.DATETIME(), nullable=True))
    op.add_column('users', sa.Column('mobile', mysql.VARCHAR(length=14), nullable=False))
    op.add_column('users', sa.Column('online', mysql.VARCHAR(length=1), nullable=False))
    op.drop_table('user')
    # ### end Alembic commands ###