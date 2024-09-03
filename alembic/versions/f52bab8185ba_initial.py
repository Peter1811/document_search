"""Initial

Revision ID: f52bab8185ba
Revises: 
Create Date: 2024-09-03 14:34:37.834141

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f52bab8185ba'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('document_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(), nullable=True),
    sa.Column('created_data', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_document_table_id'), 'document_table', ['id'], unique=False)
    op.create_index(op.f('ix_document_table_text'), 'document_table', ['text'], unique=False)
    op.create_table('rubric_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('document_rubric_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('document_id', sa.Integer(), nullable=True),
    sa.Column('rubric_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['document_id'], ['document_table.id'], ),
    sa.ForeignKeyConstraint(['rubric_id'], ['rubric_table.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('document_rubric_table')
    op.drop_table('rubric_table')
    op.drop_index(op.f('ix_document_table_text'), table_name='document_table')
    op.drop_index(op.f('ix_document_table_id'), table_name='document_table')
    op.drop_table('document_table')
    # ### end Alembic commands ###
