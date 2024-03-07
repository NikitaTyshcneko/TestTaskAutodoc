"""add user_item

Revision ID: eca6f5386e0a
Revises: 235046beb8a1
Create Date: 2024-03-07 13:05:16.486232

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eca6f5386e0a'
down_revision: Union[str, None] = '235046beb8a1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('item_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['item_id'], ['items.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_item_id'), 'user_item', ['id'], unique=False)
    op.drop_table('user_item_association')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_item_association',
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('item_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['item_id'], ['items.id'], name='user_item_association_item_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='user_item_association_user_id_fkey')
    )
    op.drop_index(op.f('ix_user_item_id'), table_name='user_item')
    op.drop_table('user_item')
    # ### end Alembic commands ###