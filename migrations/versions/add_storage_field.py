"""Add storage field

Revision ID: add_storage_field
Revises: 
Create Date: 2025-05-26 22:20:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_storage_field'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Adiciona a coluna storage com valor padrão '128GB'
    op.add_column('product', sa.Column('storage', sa.String(50), nullable=False, server_default='128GB'))
    
    # Se a coluna color não for NOT NULL, altera para NOT NULL com valor padrão 'Preto'
    with op.batch_alter_table('product') as batch_op:
        batch_op.alter_column('color', 
                            existing_type=sa.VARCHAR(50), 
                            nullable=False,
                            server_default='Preto')


def downgrade():
    # Remove a coluna storage
    op.drop_column('product', 'storage')
    
    # Reverte a coluna color para nullable
    with op.batch_alter_table('product') as batch_op:
        batch_op.alter_column('color', 
                            existing_type=sa.VARCHAR(50), 
                            nullable=True,
                            server_default=None)
